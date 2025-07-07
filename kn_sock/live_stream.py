import socket
import threading
import time
import os

# Dependency checks
try:
    import cv2
    import numpy as np
    import pyaudio
    import wave
    import subprocess
except ImportError as e:
    missing = str(e).split("No module named ")[-1].replace("'", "")
    raise ImportError(f"[kn_sock.live_stream] Missing required package: {missing}. Please install it to use live streaming.")

class LiveStreamServer:
    """
    A server that streams video and audio from a file to multiple clients.
    Automatically extracts audio from the video file using FFmpeg.
    """
    def __init__(self, video_path, host='0.0.0.0', video_port=8000, audio_port=8001):
        self.video_path = video_path
        self.audio_path = "temp_audio.wav"
        self.host = host
        self.video_port = video_port
        self.audio_port = audio_port
        self.clients = []
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._running = threading.Event()
        self._extract_audio()

    def _extract_audio(self):
        print("[*] Extracting audio from video file...")
        command = [
            'ffmpeg',
            '-i', self.video_path,
            '-y',
            '-f', 'wav',
            '-ac', '2',
            '-ar', '44100',
            '-vn',
            self.audio_path
        ]
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f"[*] Audio extracted successfully to {self.audio_path}")
        except FileNotFoundError:
            print("[!] ERROR: ffmpeg command not found. Please install FFmpeg and ensure it's in your system's PATH.")
            raise
        except subprocess.CalledProcessError as e:
            print(f"[!] ERROR: ffmpeg failed to extract audio. Error:\n{e.stderr.decode()}")
            raise

    def start(self):
        self._running.set()
        self.video_socket.bind((self.host, self.video_port))
        self.video_socket.listen(5)
        print(f"[*] Video server listening on {self.host}:{self.video_port}")
        self.audio_socket.bind((self.host, self.audio_port))
        self.audio_socket.listen(5)
        print(f"[*] Audio server listening on {self.host}:{self.audio_port}")
        video_thread = threading.Thread(target=self._accept_clients, args=(self.video_socket, "video"), daemon=True)
        audio_thread = threading.Thread(target=self._accept_clients, args=(self.audio_socket, "audio"), daemon=True)
        video_thread.start()
        audio_thread.start()

    def stop(self):
        self._running.clear()
        for client_socket in self.clients:
            try:
                client_socket.close()
            except socket.error:
                pass
        self.video_socket.close()
        self.audio_socket.close()
        try:
            if os.path.exists(self.audio_path):
                os.remove(self.audio_path)
                print(f"[*] Deleted temporary audio file: {self.audio_path}")
        except OSError as e:
            print(f"[!] Error removing temporary audio file: {e}")
        print("[*] Server stopped.")

    def _accept_clients(self, server_socket, stream_type):
        while self._running.is_set():
            try:
                client_socket, addr = server_socket.accept()
                print(f"[*] Accepted {stream_type} connection from {addr[0]}:{addr[1]}")
                self.clients.append(client_socket)
                handler_thread = threading.Thread(target=self._handle_client, args=(client_socket, stream_type), daemon=True)
                handler_thread.start()
            except socket.error:
                break

    def _handle_client(self, client_socket, stream_type):
        try:
            if stream_type == "video":
                self._stream_video(client_socket)
            elif stream_type == "audio":
                self._stream_audio(client_socket)
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            print(f"[*] Client disconnected from {stream_type} stream.")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()

    def _stream_video(self, client_socket):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print(f"[!] Could not open video file: {self.video_path}. Try converting it to mp4 (H.264) format for best compatibility.")
            return
        while self._running.is_set():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            data = np.array(buffer).tobytes()
            try:
                client_socket.sendall(len(data).to_bytes(4, 'big') + data)
            except (socket.error, BrokenPipeError):
                break
            time.sleep(1/30)
        cap.release()

    def _stream_audio(self, client_socket):
        try:
            with wave.open(self.audio_path, 'rb') as wf:
                chunk_size = 1024
                while self._running.is_set():
                    data = wf.readframes(chunk_size)
                    if not data:
                        wf.rewind()
                        data = wf.readframes(chunk_size)
                    try:
                        client_socket.sendall(data)
                    except (socket.error, BrokenPipeError):
                        break
        except FileNotFoundError:
            return

def start_live_stream(port, video_path, host='0.0.0.0', audio_port=None):
    """
    Starts a live stream server for the given video file.
    Args:
        port (int): Port for video stream.
        video_path (str): Path to video file.
        host (str): Host to bind (default 0.0.0.0).
        audio_port (int): Port for audio stream (default: port+1).
    """
    if audio_port is None:
        audio_port = port + 1
    server = LiveStreamServer(video_path, host, port, audio_port)
    try:
        server.start()
        print("[kn_sock] Live stream server started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\n[kn_sock] Stopping live stream server...")
    finally:
        server.stop()

class LiveStreamClient:
    """
    A client that receives and plays back video and audio streams from a server.
    """
    def __init__(self, host='127.0.0.1', video_port=8000, audio_port=8001):
        self.host = host
        self.video_port = video_port
        self.audio_port = audio_port
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._running = threading.Event()
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=2,
                                  rate=44100,
                                  output=True,
                                  frames_per_buffer=1024)

    def start(self):
        self._running.set()
        try:
            self.video_socket.connect((self.host, self.video_port))
            print("[*] Connected to video stream.")
            self.audio_socket.connect((self.host, self.audio_port))
            print("[*] Connected to audio stream.")
        except ConnectionRefusedError:
            print("[!] Connection refused. Make sure the server is running.")
            return
        video_thread = threading.Thread(target=self._receive_video)
        audio_thread = threading.Thread(target=self._receive_audio)
        video_thread.start()
        audio_thread.start()

    def stop(self):
        self._running.clear()
        self.video_socket.close()
        self.audio_socket.close()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        try:
            import cv2
            cv2.destroyAllWindows()
        except Exception:
            pass
        print("[*] Client stopped.")

    def _receive_video(self):
        data = b''
        payload_size = 4
        while self._running.is_set():
            try:
                while len(data) < payload_size:
                    packet = self.video_socket.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet
                if not data:
                    break
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = int.from_bytes(packed_msg_size, 'big')
                while len(data) < msg_size:
                    data += self.video_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('Live Stream', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop()
                    break
            except (ConnectionResetError, BrokenPipeError):
                print("[!] Lost connection to video stream.")
                break
        self.stop()

    def _receive_audio(self):
        chunk_size = 1024
        while self._running.is_set():
            try:
                data = self.audio_socket.recv(chunk_size)
                if not data:
                    break
                self.stream.write(data)
            except (ConnectionResetError, BrokenPipeError):
                print("[!] Lost connection to audio stream.")
                break

def connect_to_live_server(ip, port, audio_port=None):
    """
    Connects to a live stream server and plays the video/audio.
    Args:
        ip (str): Server IP address.
        port (int): Video port.
        audio_port (int): Audio port (default: port+1).
    """
    if audio_port is None:
        audio_port = port + 1
    client = LiveStreamClient(ip, port, audio_port)
    try:
        client.start()
        print("[kn_sock] Connected to live stream. Press 'q' in the video window or Ctrl+C to stop.")
        while client._running.is_set():
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\n[kn_sock] Stopping live stream client...")
    finally:
        client.stop() 