import argparse
import sys
from kn_sock import start_live_stream
import os

# Dynamically import start_live_stream from kn_sock/live_stream.py
#spec = importlib.util.spec_from_file_location(
#    "live_stream", os.path.join(os.path.dirname(__file__), "..", "kn_sock", "live_stream.py")
#)
#live_stream = importlib.util.module_from_spec(spec)
#sys.modules["live_stream"] = live_stream
#spec.loader.exec_module(live_stream)
#start_live_stream = live_stream.start_live_stream

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a live video/audio stream server using kn_sock.")
    parser.add_argument("port", type=int, help="Port for video stream (audio will use port+1 by default)")
    parser.add_argument("video_path", type=str, help="Path to video file to stream")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    parser.add_argument("--audio-port", type=int, default=None, help="Port for audio stream (default: port+1)")
    args = parser.parse_args()

    print(f"[examples/server_live.py] Starting live stream server on {args.host}:{args.port} (audio: {args.audio_port or args.port+1}) for video: {args.video_path}")
    start_live_stream(args.port, args.video_path, host=args.host, audio_port=args.audio_port) 