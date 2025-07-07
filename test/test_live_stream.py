import os
import tempfile
import pytest
from unittest.mock import patch

try:
    import cv2
    import pyaudio
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
            assert server.video_path == video_path
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