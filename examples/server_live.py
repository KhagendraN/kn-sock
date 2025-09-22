import sys
import time
from kn_sock.live_stream import LiveStreamServer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python server_live.py <video_path1> [<video_path2> ...] [video_port] [audio_port] [control_port]"
        )
        sys.exit(1)
    # Accept multiple video files
    video_paths = []
    idx = 1
    while idx < len(sys.argv) and not sys.argv[idx].isdigit():
        video_paths.append(sys.argv[idx])
        idx += 1
    if not video_paths:
        print("[!] No video files provided.")
        sys.exit(1)
    video_port = int(sys.argv[idx]) if idx < len(sys.argv) else 8000
    audio_port = int(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) else 8001
    control_port = (
        int(sys.argv[idx + 2]) if idx + 2 < len(sys.argv) else video_port + 10
    )
    print(
        f"[*] Starting LiveStreamServer with adaptive bitrate (control port: {control_port})..."
    )
    print(
        "[*] Clients will send buffer feedback to help the server adjust video quality dynamically."
    )
    print(f"[*] Serving videos: {', '.join(video_paths)}")
    server = LiveStreamServer(
        video_paths,
        video_port=video_port,
        audio_port=audio_port,
        control_port=control_port,
    )
    try:
        server.start()
        print("[kn_sock] Live stream server started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\n[kn_sock] Stopping live stream server...")
    finally:
        server.stop()
