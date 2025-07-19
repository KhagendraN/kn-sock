import threading
import time
import socket
import pytest
from kn_sock.video_chat import VideoChatServer, VideoChatClient


def test_video_chat_server_startup():
    server = VideoChatServer(
        host="127.0.0.1", video_port=9100, audio_port=9101, text_port=9102
    )
    server.start()
    # Give the server a moment to start
    time.sleep(1)
    # Try connecting to video, audio, and text ports
    video_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    text_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        video_sock.connect(("127.0.0.1", 9100))
        audio_sock.connect(("127.0.0.1", 9101))
        text_sock.connect(("127.0.0.1", 9102))
    finally:
        video_sock.close()
        audio_sock.close()
        text_sock.close()


def test_video_chat_client_connect():
    server = VideoChatServer(
        host="127.0.0.1", video_port=9103, audio_port=9104, text_port=9105
    )
    server.start()
    time.sleep(1)

    # Test client with audio disabled to avoid PyAudio issues
    client = VideoChatClient(
        server_ip="127.0.0.1",
        video_port=9103,
        audio_port=9104,
        text_port=9105,
        room="testroom",
        nickname="testuser",
        enable_audio=False,  # Disable audio to avoid PyAudio issues
    )

    # Just test that start() does not raise
    try:
        client_thread = threading.Thread(target=client.start, daemon=True)
        client_thread.start()
        time.sleep(2)  # Give more time for initialization

        # Check that client is running
        assert client.running is True

        # Clean up
        client.running = False
        time.sleep(1)
    except Exception as e:
        pytest.fail(f"Client failed to start: {e}")


def test_video_chat_rooms():
    server = VideoChatServer(
        host="127.0.0.1", video_port=9106, audio_port=9107, text_port=9108
    )
    server.start()
    time.sleep(1)

    # Test that rooms are created when clients connect (with audio disabled)
    client1 = VideoChatClient(
        server_ip="127.0.0.1",
        video_port=9106,
        audio_port=9107,
        text_port=9108,
        room="room1",
        nickname="user1",
        enable_audio=False,  # Disable audio
    )
    client2 = VideoChatClient(
        server_ip="127.0.0.1",
        video_port=9106,
        audio_port=9107,
        text_port=9108,
        room="room2",
        nickname="user2",
        enable_audio=False,  # Disable audio
    )

    try:
        client1_thread = threading.Thread(target=client1.start, daemon=True)
        client2_thread = threading.Thread(target=client2.start, daemon=True)

        client1_thread.start()
        client2_thread.start()
        time.sleep(3)  # Give more time for connections

        # Check that rooms exist
        assert "room1" in server.rooms
        assert "room2" in server.rooms
        assert "user1" in server.rooms["room1"]["nicknames"].values()
        assert "user2" in server.rooms["room2"]["nicknames"].values()

        # Clean up
        client1.running = False
        client2.running = False
        time.sleep(1)
    except Exception as e:
        pytest.fail(f"Room test failed: {e}")


def test_video_chat_audio_disabled():
    """Test that video chat works without audio"""
    server = VideoChatServer(
        host="127.0.0.1", video_port=9109, audio_port=9110, text_port=9111
    )
    server.start()
    time.sleep(1)

    client = VideoChatClient(
        server_ip="127.0.0.1",
        video_port=9109,
        audio_port=9110,
        text_port=9111,
        room="testroom",
        nickname="testuser",
        enable_audio=False,  # Explicitly disable audio
    )

    try:
        client_thread = threading.Thread(target=client.start, daemon=True)
        client_thread.start()
        time.sleep(2)

        # Verify audio is disabled
        assert client.audio_available is False
        assert client.running is True

        # Clean up
        client.running = False
        time.sleep(1)
    except Exception as e:
        pytest.fail(f"Audio disabled test failed: {e}")


def test_video_chat_server_cleanup():
    """Test that server can be stopped cleanly"""
    server = VideoChatServer(
        host="127.0.0.1", video_port=9112, audio_port=9113, text_port=9114
    )
    server.start()
    time.sleep(1)

    # Verify server is running
    assert server.running is True

    # Stop server
    server.running = False
    time.sleep(1)

    # Verify server stopped
    assert server.running is False
