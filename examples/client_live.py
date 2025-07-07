import argparse
import sys
from kn_sock import connect_to_live_server
import os

# Dynamically import connect_to_live_server from kn_sock/live_stream.py
#spec = importlib.util.spec_from_file_location(
#    "live_stream", os.path.join(os.path.dirname(__file__), "..", "kn_sock", "live_stream.py")
#)
#live_stream = importlib.util.module_from_spec(spec)
#sys.modules["live_stream"] = live_stream
#spec.loader.exec_module(live_stream)
#connect_to_live_server = live_stream.connect_to_live_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to a live video/audio stream server using kn_sock.")
    parser.add_argument("ip", type=str, help="Server IP address")
    parser.add_argument("port", type=int, help="Video port (audio will use port+1 by default)")
    parser.add_argument("--audio-port", type=int, default=None, help="Audio port (default: port+1)")
    args = parser.parse_args()

    print(f"[examples/client_live.py] Connecting to live stream at {args.ip}:{args.port} (audio: {args.audio_port or args.port+1})")
    connect_to_live_server(args.ip, args.port, audio_port=args.audio_port) 