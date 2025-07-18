import socket
import threading
import pickle
import struct
import cv2
import pyaudio
import time
import numpy as np
import os

# Set display backend for OpenCV to avoid Qt issues
os.environ["QT_QPA_PLATFORM"] = "xcb"

# Video settings
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
FRAME_RATE = 15

# Audio settings
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Changed from 16000 to 44100
CHUNK = 1024


class VideoChatServer:
    def __init__(
        self, host="0.0.0.0", video_port=9000, audio_port=9001, text_port=9002
    ):
        self.host = host
        self.video_port = video_port
        self.audio_port = audio_port
        self.text_port = text_port
        self.rooms = (
            {}
        )  # room_name -> { 'video': [clients], 'audio': [clients], 'text': [clients], 'nicknames': {sock: name} }
        self.lock = threading.Lock()
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._video_server, daemon=True).start()
        threading.Thread(target=self._audio_server, daemon=True).start()
        threading.Thread(target=self._text_server, daemon=True).start()

    def _video_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.video_port))
        s.listen(5)
        while self.running:
            client, _ = s.accept()
            threading.Thread(
                target=self._handle_video_client, args=(client,), daemon=True
            ).start()

    def _audio_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.audio_port))
        s.listen(5)
        while self.running:
            client, _ = s.accept()
            threading.Thread(
                target=self._handle_audio_client, args=(client,), daemon=True
            ).start()

    def _text_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.text_port))
        s.listen(5)
        while self.running:
            client, _ = s.accept()
            threading.Thread(
                target=self._handle_text_client, args=(client,), daemon=True
            ).start()

    def _handle_video_client(self, client):
        room, nickname = self._recv_handshake(client)
        if not room or not nickname:
            client.close()
            return
        with self.lock:
            if room not in self.rooms:
                self.rooms[room] = {
                    "video": [],
                    "audio": [],
                    "text": [],
                    "nicknames": {},
                }
            self.rooms[room]["video"].append(client)
            self.rooms[room]["nicknames"][client] = nickname
        try:
            while self.running:
                data = self._recv_msg(client)
                if not data:
                    break
                # Broadcast to all other clients in the same room
                with self.lock:
                    for c in self.rooms[room]["video"]:
                        if c != client:
                            try:
                                self._send_msg(c, data)
                            except:
                                pass
        finally:
            with self.lock:
                if client in self.rooms[room]["video"]:
                    self.rooms[room]["video"].remove(client)
                if client in self.rooms[room]["nicknames"]:
                    del self.rooms[room]["nicknames"][client]
            client.close()

    def _handle_audio_client(self, client):
        room, nickname = self._recv_handshake(client)
        if not room or not nickname:
            client.close()
            return
        with self.lock:
            if room not in self.rooms:
                self.rooms[room] = {
                    "video": [],
                    "audio": [],
                    "text": [],
                    "nicknames": {},
                }
            self.rooms[room]["audio"].append(client)
            self.rooms[room]["nicknames"][client] = nickname
        try:
            while self.running:
                data = self._recv_msg(client)
                if not data:
                    break
                # Broadcast to all other clients in the same room
                with self.lock:
                    for c in self.rooms[room]["audio"]:
                        if c != client:
                            try:
                                self._send_msg(c, data)
                            except:
                                pass
        finally:
            with self.lock:
                if client in self.rooms[room]["audio"]:
                    self.rooms[room]["audio"].remove(client)
                if client in self.rooms[room]["nicknames"]:
                    del self.rooms[room]["nicknames"][client]
            client.close()

    def _handle_text_client(self, client):
        room, nickname = self._recv_handshake(client)
        if not room or not nickname:
            client.close()
            return
        with self.lock:
            if room not in self.rooms:
                self.rooms[room] = {
                    "video": [],
                    "audio": [],
                    "text": [],
                    "nicknames": {},
                }
            self.rooms[room]["text"].append(client)
            self.rooms[room]["nicknames"][client] = nickname
        try:
            while self.running:
                data = self._recv_msg(client)
                if not data:
                    break
                # Broadcast to all other clients in the same room
                with self.lock:
                    for c in self.rooms[room]["text"]:
                        if c != client:
                            try:
                                self._send_msg(c, data)
                            except:
                                pass
        finally:
            with self.lock:
                if client in self.rooms[room]["text"]:
                    self.rooms[room]["text"].remove(client)
                if client in self.rooms[room]["nicknames"]:
                    del self.rooms[room]["nicknames"][client]
            client.close()

    def _recv_handshake(self, sock):
        # Expect a pickled dict: {'room': str, 'nickname': str}
        try:
            data = self._recv_msg(sock)
            if not data:
                return None, None
            info = pickle.loads(data)
            return info.get("room"), info.get("nickname")
        except Exception:
            return None, None

    def _send_msg(self, sock, data):
        msg = struct.pack(">I", len(data)) + data
        sock.sendall(msg)

    def _recv_msg(self, sock):
        raw_msglen = self._recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack(">I", raw_msglen)[0]
        return self._recvall(sock, msglen)

    def _recvall(self, sock, n):
        data = b""
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data


def safe_audio_init():
    """Safely initialize PyAudio with error handling"""
    try:
        pa = pyaudio.PyAudio()
        # Test if PyAudio is working by getting device count
        device_count = pa.get_device_count()
        return pa, True
    except Exception as e:
        print(f"PyAudio initialization failed: {e}")
        return None, False


def find_working_audio_device(pa, is_input=True):
    """Find a working audio device with better error handling"""
    try:
        device_count = pa.get_device_count()
        if device_count == 0:
            return None

        # Try to find a working device
        for i in range(device_count):
            try:
                device_info = pa.get_device_info_by_index(i)
                if is_input and device_info["maxInputChannels"] > 0:
                    # Test if we can open this device
                    test_stream = pa.open(
                        format=AUDIO_FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=is_input,
                        output=not is_input,
                        input_device_index=i if is_input else None,
                        output_device_index=i if not is_input else None,
                        frames_per_buffer=CHUNK,
                    )
                    test_stream.close()
                    return i
                elif not is_input and device_info["maxOutputChannels"] > 0:
                    # Test if we can open this device
                    test_stream = pa.open(
                        format=AUDIO_FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=is_input,
                        output=not is_input,
                        input_device_index=i if is_input else None,
                        output_device_index=i if not is_input else None,
                        frames_per_buffer=CHUNK,
                    )
                    test_stream.close()
                    return i
            except Exception:
                continue
        return None
    except Exception:
        return None


def get_audio_devices():
    """Get list of available audio devices"""
    try:
        pa = pyaudio.PyAudio()
        devices = []
        for i in range(pa.get_device_count()):
            try:
                device_info = pa.get_device_info_by_index(i)
                devices.append(
                    {
                        "index": i,
                        "name": device_info["name"],
                        "maxInputChannels": device_info["maxInputChannels"],
                        "maxOutputChannels": device_info["maxOutputChannels"],
                        "defaultSampleRate": device_info["defaultSampleRate"],
                    }
                )
            except:
                continue
        pa.terminate()
        return devices
    except:
        return []


def find_best_audio_devices():
    """Find the best input and output devices"""
    devices = get_audio_devices()
    input_device = None
    output_device = None

    # Look for devices with good sample rate support
    for device in devices:
        if device["maxInputChannels"] > 0 and input_device is None:
            # Prefer devices that support 44100 Hz
            if abs(device["defaultSampleRate"] - 44100) < 100:
                input_device = device["index"]
            elif input_device is None:
                input_device = device["index"]

        if device["maxOutputChannels"] > 0 and output_device is None:
            # Prefer devices that support 44100 Hz
            if abs(device["defaultSampleRate"] - 44100) < 100:
                output_device = device["index"]
            elif output_device is None:
                output_device = device["index"]

    return input_device, output_device


class VideoChatClient:
    def __init__(
        self,
        server_ip,
        video_port=9000,
        audio_port=9001,
        text_port=9002,
        room="main",
        nickname="user",
        enable_audio=True,
    ):
        self.server_ip = server_ip
        self.video_port = video_port
        self.audio_port = audio_port
        self.text_port = text_port
        self.room = room
        self.nickname = nickname
        self.video_sock = None
        self.audio_sock = None
        self.text_sock = None
        self.running = False
        self.chat_messages = []
        self.chat_lock = threading.Lock()
        self.video_enabled = True
        self.audio_enabled = True
        self.controls_lock = threading.Lock()
        self.audio_available = enable_audio
        self.video_available = True

    def start(self):
        self.running = True
        self.video_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_sock.connect((self.server_ip, self.video_port))
        self.audio_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_sock.connect((self.server_ip, self.audio_port))
        self.text_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.text_sock.connect((self.server_ip, self.text_port))
        self._send_handshake(self.video_sock)
        self._send_handshake(self.audio_sock)
        self._send_handshake(self.text_sock)
        threading.Thread(target=self._send_video, daemon=True).start()
        threading.Thread(target=self._recv_video, daemon=True).start()
        if self.audio_available:
            threading.Thread(target=self._send_audio, daemon=True).start()
            threading.Thread(target=self._recv_audio, daemon=True).start()
        threading.Thread(target=self._recv_text, daemon=True).start()
        threading.Thread(target=self._send_text_input, daemon=True).start()

    def _send_handshake(self, sock):
        info = {"room": self.room, "nickname": self.nickname}
        data = pickle.dumps(info)
        self._send_msg(sock, data)

    def _send_video(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Warning: Could not open camera. Video will be disabled.")
                self.video_available = False
                cap.release()
                return

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
            cap.set(cv2.CAP_PROP_FPS, FRAME_RATE)

            while self.running:
                with self.controls_lock:
                    if self.video_enabled and self.video_available:
                        ret, frame = cap.read()
                        if not ret:
                            continue
                        data = pickle.dumps(frame)
                        self._send_msg(self.video_sock, data)
                    else:
                        # Send a black frame when video is disabled
                        black_frame = np.zeros(
                            (FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8
                        )
                        data = pickle.dumps(black_frame)
                        self._send_msg(self.video_sock, data)
            cap.release()
        except Exception as e:
            print(f"Video error: {e}")
            self.video_available = False

    def _recv_video(self):
        try:
            cv2.namedWindow(f"Video Chat [{self.room}]", cv2.WINDOW_NORMAL)
            print("Controls: 'm' to mute/unmute, 'v' to toggle video, 'q' to quit")
            while self.running:
                data = self._recv_msg(self.video_sock)
                if not data:
                    continue
                frame = pickle.loads(data)
                # Add chat overlay
                frame = self._add_chat_overlay(frame)
                # Add controls overlay
                frame = self._add_controls_overlay(frame)
                cv2.imshow(f"Video Chat [{self.room}]", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    self.running = False
                    break
                elif key == ord("m"):
                    with self.controls_lock:
                        self.audio_enabled = not self.audio_enabled
                        status = "muted" if not self.audio_enabled else "unmuted"
                        print(f"Audio {status}")
                elif key == ord("v"):
                    with self.controls_lock:
                        self.video_enabled = not self.video_enabled
                        status = "disabled" if not self.video_enabled else "enabled"
                        print(f"Video {status}")
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Video display error: {e}")

    def _add_chat_overlay(self, frame):
        # Add semi-transparent overlay for chat
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (frame.shape[1], 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Add chat messages
        with self.chat_lock:
            messages = self.chat_messages[-5:]  # Show last 5 messages
        y_offset = 20
        for msg in messages:
            cv2.putText(
                frame,
                msg,
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )
            y_offset += 20
        return frame

    def _add_controls_overlay(self, frame):
        # Add status indicators in top-right corner
        with self.controls_lock:
            audio_status = "MUTED" if not self.audio_enabled else "AUDIO"
            video_status = "NO VIDEO" if not self.video_enabled else "VIDEO"

        # Audio status
        color = (0, 0, 255) if not self.audio_enabled else (0, 255, 0)
        cv2.putText(
            frame,
            audio_status,
            (frame.shape[1] - 100, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
        )

        # Video status
        color = (0, 0, 255) if not self.video_enabled else (0, 255, 0)
        cv2.putText(
            frame,
            video_status,
            (frame.shape[1] - 100, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
        )

        # Controls help
        cv2.putText(
            frame,
            "m: mute/unmute, v: toggle video, q: quit",
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255, 255, 255),
            1,
        )

        return frame

    def _send_audio(self):
        if not self.audio_available:
            return

        try:
            pa, success = safe_audio_init()
            if not success:
                print("Warning: PyAudio initialization failed. Audio will be disabled.")
                self.audio_available = False
                return

            # Find the best input device
            input_device, _ = find_best_audio_devices()

            if input_device is None:
                print(
                    "Warning: No working audio input device found. Audio will be disabled."
                )
                self.audio_available = False
                pa.terminate()
                return

            print(f"Using audio input device: {input_device}")

            stream = pa.open(
                format=AUDIO_FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=input_device,
                frames_per_buffer=CHUNK,
            )

            while self.running:
                with self.controls_lock:
                    if self.audio_enabled and self.audio_available:
                        try:
                            data = stream.read(CHUNK, exception_on_overflow=False)
                            self._send_msg(self.audio_sock, data)
                        except Exception as e:
                            print(f"Audio input error: {e}")
                            break
                    else:
                        # Send silence when muted
                        silence = b"\x00" * (CHUNK * 2)  # 16-bit samples
                        self._send_msg(self.audio_sock, silence)
            stream.stop_stream()
            stream.close()
            pa.terminate()
        except Exception as e:
            print(f"Audio setup error: {e}")
            self.audio_available = False

    def _recv_audio(self):
        if not self.audio_available:
            return

        try:
            pa, success = safe_audio_init()
            if not success:
                print("Warning: PyAudio initialization failed. Audio will be disabled.")
                return

            # Find the best output device
            _, output_device = find_best_audio_devices()

            if output_device is None:
                print(
                    "Warning: No working audio output device found. Audio will be disabled."
                )
                pa.terminate()
                return

            print(f"Using audio output device: {output_device}")

            stream = pa.open(
                format=AUDIO_FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                output_device_index=output_device,
                frames_per_buffer=CHUNK,
            )

            while self.running:
                data = self._recv_msg(self.audio_sock)
                if not data:
                    continue
                try:
                    stream.write(data)
                except Exception as e:
                    print(f"Audio output error: {e}")
                    break
            stream.stop_stream()
            stream.close()
            pa.terminate()
        except Exception as e:
            print(f"Audio output setup error: {e}")

    def _recv_text(self):
        while self.running:
            data = self._recv_msg(self.text_sock)
            if not data:
                continue
            try:
                msg_data = pickle.loads(data)
                sender = msg_data.get("sender", "Unknown")
                message = msg_data.get("message", "")
                timestamp = time.strftime("%H:%M")
                chat_msg = f"[{timestamp}] {sender}: {message}"
                with self.chat_lock:
                    self.chat_messages.append(chat_msg)
                    if len(self.chat_messages) > 10:  # Keep only last 10 messages
                        self.chat_messages.pop(0)
            except:
                pass

    def _send_text_input(self):
        print(
            f"Connected to room '{self.room}' as '{self.nickname}'. Type messages and press Enter:"
        )
        while self.running:
            try:
                message = input()
                if not self.running:
                    break
                msg_data = {"sender": self.nickname, "message": message}
                data = pickle.dumps(msg_data)
                self._send_msg(self.text_sock, data)
            except (EOFError, KeyboardInterrupt):
                break
        self.running = False

    def _send_msg(self, sock, data):
        msg = struct.pack(">I", len(data)) + data
        sock.sendall(msg)

    def _recv_msg(self, sock):
        raw_msglen = self._recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack(">I", raw_msglen)[0]
        return self._recvall(sock, msglen)

    def _recvall(self, sock, n):
        data = b""
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
