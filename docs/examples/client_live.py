import sys
import time
from kn_sock.live_stream import LiveStreamClient

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python client_live.py <host> [video_port] [audio_port] [control_port]"
        )
        sys.exit(1)
    host = sys.argv[1]
    video_port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    audio_port = int(sys.argv[3]) if len(sys.argv) > 3 else 8001
    control_port = int(sys.argv[4]) if len(sys.argv) > 4 else video_port + 10
    print(
        f"[*] Connecting to LiveStreamServer with adaptive bitrate (control port: {control_port})..."
    )
    print(
        "[*] Client will send buffer feedback to help the server adjust video quality dynamically."
    )
    print(
        "[*] If the server offers multiple videos, you will be prompted to select one."
    )
    client = LiveStreamClient(host, video_port, audio_port, control_port=control_port)
    try:
        client.start()
        print(
            "[kn_sock] Connected to live stream. Press 'q' in the video window or Ctrl+C to stop."
        )
        while client._running.is_set():
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\n[kn_sock] Stopping live stream client...")
    finally:
        client.stop()
