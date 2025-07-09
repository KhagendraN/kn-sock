import socket
import threading
import time
import os
import queue
import struct
import json
from kn_sock.json_socket import send_json_response, _recv_line

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

AUDIO_MAGIC = b'AUD0'

class LiveStreamServer:
    """
    A server that streams video and audio from a file to multiple clients.
    Automatically extracts audio from the video file using FFmpeg.
    """
    def __init__(self, video_paths, host='0.0.0.0', video_port=8000, audio_port=8001, control_port=None):
        if isinstance(video_paths, str):
            video_paths = [video_paths]
        self.video_paths = video_paths
        self.audio_path = "temp_audio.wav"
        self.host = host
        self.video_port = video_port
        self.audio_port = audio_port
        self.control_port = control_port or (video_port + 10)
        self.clients = []
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._running = threading.Event()
        self._extract_audio(self.video_paths[0])
        self._client_quality = {}  # addr -> jpeg quality

    def _extract_audio(self, video_path):
        print("[*] Extracting audio from video file...")
        command = [
            'ffmpeg',
            '-i', video_path,
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
        self.control_socket.bind((self.host, self.control_port))
        self.control_socket.listen(5)
        print(f"[*] Control server listening on {self.host}:{self.control_port}")
        threading.Thread(target=self._accept_clients, args=(self.video_socket, "video"), daemon=True).start()
        threading.Thread(target=self._accept_clients, args=(self.audio_socket, "audio"), daemon=True).start()
        threading.Thread(target=self._accept_control_clients, daemon=True).start()

    def stop(self):
        self._running.clear()
        for client_socket in self.clients:
            try:
                client_socket.close()
            except socket.error:
                pass
        self.video_socket.close()
        self.audio_socket.close()
        self.control_socket.close()
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

    def _accept_control_clients(self):
        while self._running.is_set():
            try:
                client_sock, addr = self.control_socket.accept()
                print(f"[*] Accepted control connection from {addr[0]}:{addr[1]}")
                threading.Thread(target=self._handle_control_client, args=(client_sock, addr), daemon=True).start()
            except socket.error:
                break

    def _handle_control_client(self, client_sock, addr):
        # Default quality
        self._client_quality[addr] = 80
        try:
            while self._running.is_set():
                data = b''
                while not data.endswith(b'\n'):
                    chunk = client_sock.recv(1024)
                    if not chunk:
                        break
                    data += chunk
                if not data:
                    break
                try:
                    feedback = json.loads(data.decode())
                    buf_level = feedback.get("buffer_level", 0.2)
                    # Simple logic: if buffer low, reduce quality; if high, increase
                    q = self._client_quality[addr]
                    if buf_level < 0.1 and q > 40:
                        q -= 10
                    elif buf_level > 0.3 and q < 90:
                        q += 10
                    self._client_quality[addr] = max(40, min(90, q))
                except Exception:
                    continue
        finally:
            del self._client_quality[addr]
            client_sock.close()

    def _handle_client(self, client_socket, stream_type):
        try:
            if stream_type == "video":
                # Multi-video handshake
                video_names = [os.path.basename(p) for p in self.video_paths]
                send_json_response(client_socket, {"videos": video_names})
                sel_bytes = _recv_line(client_socket)
                if not sel_bytes:
                    print("[VIDEO] Client disconnected before selection.")
                    return
                try:
                    sel = int(json.loads(sel_bytes.decode().strip()).get("index", 0))
                except Exception:
                    sel = 0
                sel = max(0, min(sel, len(self.video_paths)-1))
                selected_video = self.video_paths[sel]
                print(f"[VIDEO] Client selected video: {selected_video}")
                self._extract_audio(selected_video)
                self._stream_video(client_socket, selected_video)
            elif stream_type == "audio":
                self._stream_audio(client_socket)
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            print(f"[*] Client disconnected from {stream_type} stream.")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()

    def _stream_video(self, client_socket, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"[!] Could not open video file: {video_path}. Try converting it to mp4 (H.264) format for best compatibility.")
            return
        addr = client_socket.getpeername()
        while self._running.is_set():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            quality = self._client_quality.get(addr, 80)
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
            data = np.array(buffer).tobytes()
            timestamp = time.time()
            try:
                client_socket.sendall(struct.pack('!dI', timestamp, len(data)) + data)
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
                    timestamp = time.time()
                    try:
                        # [4 bytes magic][8 bytes timestamp][4 bytes chunk_len][chunk]
                        header = AUDIO_MAGIC + struct.pack('!dI', timestamp, len(data))
                        client_socket.sendall(header + data)
                    except (socket.error, BrokenPipeError):
                        break
        except FileNotFoundError:
            return

def start_live_stream(port, video_paths, host='0.0.0.0', audio_port=None):
    """
    Starts a live stream server for the given video file(s).
    Args:
        port (int): Port for video stream.
        video_paths (list[str]): Path(s) to video file(s).
        host (str): Host to bind (default 0.0.0.0).
        audio_port (int): Port for audio stream (default: port+1).
    """
    if audio_port is None:
        audio_port = port + 1
    server = LiveStreamServer(video_paths, host, port, audio_port)
    try:
        server.start()
        print("[kn_sock] Live stream server started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\n[kn_sock] Stopping live stream server...")
    finally:
        server.stop()

class JitterBuffer:
    """
    Thread-safe buffer to smooth out irregular frame/chunk arrival times.
    Use for video/audio streaming to reduce jitter/stutter.
    """
    def __init__(self, max_delay=0.2, target_interval=1/30):
        self.buffer = queue.Queue()
        self.max_delay = max_delay  # seconds of buffer (e.g., 0.2s)
        self.target_interval = target_interval  # e.g., 1/30 for 30fps
        self._running = threading.Event()

    def start(self, process_func):
        self._running.set()
        threading.Thread(target=self._playback_loop, args=(process_func,), daemon=True).start()

    def stop(self):
        self._running.clear()
        with self.buffer.mutex:
            self.buffer.queue.clear()

    def put(self, item, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        self.buffer.put((timestamp, item))

    def _playback_loop(self, process_func):
        # Wait until buffer is filled to max_delay
        base_ts = None
        debug_count = 0
        while self._running.is_set() and self.buffer.qsize() * self.target_interval < self.max_delay:
            time.sleep(self.target_interval / 2)
        while self._running.is_set():
            try:
                ts, item = self.buffer.get(timeout=self.target_interval)
                if base_ts is None:
                    base_ts = ts
                    start_play = time.time()
                # Calculate when to play this item
                now = time.time()
                play_at = start_play + (ts - base_ts)
                delay = play_at - now
                # Sanity check: skip if delay is absurd
                if delay > 2 or delay < -2:
                    print(f"[JitterBuffer] Skipping frame/chunk due to unreasonable delay: {delay:.3f}s (ts={ts}, base_ts={base_ts})")
                    continue
                if delay > 0:
                    time.sleep(delay)
                process_func(item)
            except queue.Empty:
                continue

class LiveStreamClient:
    """
    A client that receives and plays back video and audio streams from a server.
    Now uses a JitterBuffer for smooth playback.
    """
    def __init__(self, host='127.0.0.1', video_port=8000, audio_port=8001, video_buffer_ms=200, audio_buffer_ms=200, video_fps=30, control_port=None):
        self.host = host
        self.video_port = video_port
        self.audio_port = audio_port
        self.control_port = control_port or (video_port + 10)
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._running = threading.Event()
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=2,
                                  rate=44100,
                                  output=True,
                                  frames_per_buffer=1024)
        self.video_jitter = JitterBuffer(max_delay=video_buffer_ms/1000, target_interval=1/video_fps)
        self.audio_jitter = JitterBuffer(max_delay=audio_buffer_ms/1000, target_interval=1024/44100)

    def start(self):
        self._running.set()
        try:
            self.video_socket.connect((self.host, self.video_port))
            print("[*] Connected to video stream.")
            # Multi-video handshake
            video_list_bytes = _recv_line(self.video_socket)
            video_list = json.loads(video_list_bytes.decode().strip())
            videos = video_list.get("videos", [])
            if len(videos) > 1:
                print("Available videos:")
                for i, v in enumerate(videos):
                    print(f"  {i}: {v}")
                while True:
                    try:
                        sel = int(input(f"Select video [0-{len(videos)-1}]: "))
                        if 0 <= sel < len(videos):
                            break
                    except Exception:
                        pass
                sel_json = json.dumps({"index": sel}) + '\n'
                self.video_socket.sendall(sel_json.encode('utf-8'))
            else:
                self.video_socket.sendall(json.dumps({"index": 0}).encode('utf-8') + b'\n')
            self.audio_socket.connect((self.host, self.audio_port))
            print("[*] Connected to audio stream.")
            self.control_socket.connect((self.host, self.control_port))
            print("[*] Connected to control channel.")
        except ConnectionRefusedError:
            print("[!] Connection refused. Make sure the server is running.")
            return
        self.video_jitter.start(self._play_video_frame)
        self.audio_jitter.start(self._play_audio_chunk)
        threading.Thread(target=self._send_feedback_loop, daemon=True).start()
        video_thread = threading.Thread(target=self._receive_video)
        audio_thread = threading.Thread(target=self._receive_audio)
        video_thread.start()
        audio_thread.start()

    def stop(self):
        self._running.clear()
        try:
            self.video_socket.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            self.audio_socket.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            self.control_socket.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        self.video_socket.close()
        self.audio_socket.close()
        self.control_socket.close()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.video_jitter.stop()
        self.audio_jitter.stop()
        try:
            import cv2
            cv2.destroyAllWindows()
        except Exception:
            pass
        print("[*] Client stopped.")

    def _play_video_frame(self, frame):
        import cv2
        cv2.imshow('Live Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.stop()

    def _play_audio_chunk(self, chunk):
        self.stream.write(chunk)

    def _send_feedback_loop(self):
        while self._running.is_set():
            # Feedback: buffer fill level (in seconds)
            buf_level = self.video_jitter.buffer.qsize() * self.video_jitter.target_interval
            msg = json.dumps({"buffer_level": buf_level}) + '\n'
            try:
                self.control_socket.sendall(msg.encode())
            except Exception:
                break
            time.sleep(1)

    def _receive_video(self):
        import cv2
        data = b''
        payload_size = 12  # 8 bytes timestamp + 4 bytes length
        while self._running.is_set():
            try:
                while len(data) < payload_size:
                    packet = self.video_socket.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet
                if not data:
                    break
                packed = data[:payload_size]
                data = data[payload_size:]
                timestamp, msg_size = struct.unpack('!dI', packed)
                while len(data) < msg_size:
                    data += self.video_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
                self.video_jitter.put(frame, timestamp=timestamp)
            except (ConnectionResetError, BrokenPipeError):
                print("[!] Lost connection to video stream.")
                break
        self.stop()

    def _receive_audio(self):
        chunk_size = 1024
        ts_size = 8
        magic_size = 4
        len_size = 4
        data = b''
        debug_count = 0
        while self._running.is_set():
            try:
                # Find magic number
                while len(data) < magic_size:
                    packet = self.audio_socket.recv(magic_size - len(data))
                    if not packet:
                        print("[AUDIO] Socket closed while reading magic.")
                        return
                    data += packet
                if data[:magic_size] != AUDIO_MAGIC:
                    # Shift by one and try again
                    data = data[1:]
                    continue
                data = data[magic_size:]
                # Read timestamp and chunk_len
                while len(data) < ts_size + len_size:
                    packet = self.audio_socket.recv(ts_size + len_size - len(data))
                    if not packet:
                        print("[AUDIO] Socket closed while reading header.")
                        return
                    data += packet
                # timestamp = struct.unpack('!d', data[:ts_size])[0]  # Ignore timestamp for audio
                chunk_len = struct.unpack('!I', data[ts_size:ts_size+len_size])[0]
                data = data[ts_size+len_size:]
                # Read chunk
                while len(data) < chunk_len:
                    packet = self.audio_socket.recv(chunk_len - len(data))
                    if not packet:
                        print("[AUDIO] Socket closed while reading chunk.")
                        return
                    data += packet
                chunk = data[:chunk_len]
                data = data[chunk_len:]
                if debug_count < 5:
                    print(f"[AUDIO][DEBUG] chunk_size={len(chunk)}")
                    debug_count += 1
                self.stream.write(chunk)
            except (ConnectionResetError, BrokenPipeError):
                print("[!] Lost connection to audio stream.")
                break
            except Exception as e:
                print(f"[AUDIO][ERROR] {e}")
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