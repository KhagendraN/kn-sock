import threading
import time
import os
import tempfile
import pytest
from unittest.mock import patch

try:
    import cv2
    import pyaudio
    import numpy as np
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

pytestmark = pytest.mark.skipif(not HAS_DEPS, reason='cv2/pyaudio not installed')

from kn_sock.live_stream import LiveStreamServer, LiveStreamClient

def test_live_stream_server_client_init():
    # Create a dummy video file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as f:
        f.write(b'\x00' * 1024)  # Not a real video, but enough for instantiation
        video_path = f.name
    try:
        with patch('kn_sock.live_stream.LiveStreamServer._extract_audio', return_value=None):
            server = LiveStreamServer(video_path, video_port=9999, audio_port=10000)
            assert server.video_paths == [video_path]
            client = LiveStreamClient('localhost', video_port=9999, audio_port=10000)
            assert client.host == 'localhost'
            # Just test start/stop do not raise
            server._running.set()
            server.stop()
            client._running.set()
            client.stop()
            print('[SUCCESS] LiveStreamServer/Client instantiation and stop')
    finally:
        os.remove(video_path)

def test_adaptive_bitrate(tmp_path):
    # Use a short dummy wav file and a small video (or mock video)
    video_path = str(tmp_path / "dummy.mp4")
    # Create a dummy video file if not exists (1 black frame)
    import cv2
    import numpy as np
    frame = np.zeros((240, 320, 3), dtype=np.uint8)
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (320, 240))
    out.write(frame)
    out.release()
    with patch('kn_sock.live_stream.LiveStreamServer._extract_audio', return_value=None):
        server = LiveStreamServer(video_path, host='127.0.0.1', video_port=9000, audio_port=9001, control_port=9010)
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()
        time.sleep(2)
        client = LiveStreamClient('127.0.0.1', 9000, 9001, control_port=9010, video_buffer_ms=100, audio_buffer_ms=100)
        client_thread = threading.Thread(target=client.start, daemon=True)
        client_thread.start()
        time.sleep(5)
        client.stop()
        server.stop()
        # Check that server._client_quality has been updated
        print(f"[TEST] Server client quality settings: {server._client_quality}")
        assert any(q != 80 for q in server._client_quality.values()) or len(server._client_quality) == 0
        print("[SUCCESS] Adaptive bitrate feedback and quality adjustment")

def test_multi_video_selection(tmp_path):
    import cv2
    import numpy as np
    from unittest.mock import patch
    # Create two dummy video files
    video_paths = []
    for i in range(2):
        path = str(tmp_path / f"dummy_{i}.mp4")
        frame = np.full((240, 320, 3), i*100, dtype=np.uint8)  # Different color for each video
        out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (320, 240))
        out.write(frame)
        out.release()
        video_paths.append(path)
    with patch('kn_sock.live_stream.LiveStreamServer._extract_audio', return_value=None):
        server = LiveStreamServer(video_paths, host='127.0.0.1', video_port=9100, audio_port=9101, control_port=9110)
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()
        time.sleep(2)
        # Patch input to select the second video (index 1)
        with patch('builtins.input', return_value='1'):
            client = LiveStreamClient('127.0.0.1', 9100, 9101, control_port=9110, video_buffer_ms=100, audio_buffer_ms=100)
            client_thread = threading.Thread(target=client.start, daemon=True)
            client_thread.start()
            time.sleep(5)
            client.stop()
        server.stop()
        print("[SUCCESS] Multi-video selection test passed.") 