"""
Live Streaming Example

Demonstrates live video/audio streaming using kn-sock's live stream server/client.

How to run:
    # Start the server (specify video file)
    python live_streaming.py server <video_file>

    # Start the client (in another terminal)
    python live_streaming.py client
"""
import sys
from kn_sock import start_live_stream, connect_to_live_server


def server():
    if len(sys.argv) < 3:
        print("Usage: python live_streaming.py server <video_file>")
        sys.exit(1)
    video_file = sys.argv[2]
    start_live_stream(9600, [video_file])


def client():
    connect_to_live_server("localhost", 9600)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python live_streaming.py [server <video_file>|client]")
        sys.exit(1)
    if sys.argv[1] == "server":
        server()
    else:
        client()
