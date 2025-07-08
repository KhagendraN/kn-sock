import sys
import time
from kn_sock.live_stream import LiveStreamServer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python server_live.py <video_path> [video_port] [audio_port] [control_port]")
        sys.exit(1)
    video_path = sys.argv[1]
    video_port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    audio_port = int(sys.argv[3]) if len(sys.argv) > 3 else 8001
    control_port = int(sys.argv[4]) if len(sys.argv) > 4 else video_port + 10
    print(f"[*] Starting LiveStreamServer with adaptive bitrate (control port: {control_port})...")
    print("[*] Clients will send buffer feedback to help the server adjust video quality dynamically.")
    server = LiveStreamServer(video_path, video_port=video_port, audio_port=audio_port, control_port=control_port)
    try:
        server.start()
        print("[kn_sock] Live stream server started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\n[kn_sock] Stopping live stream server...")
    finally:
        server.stop() 