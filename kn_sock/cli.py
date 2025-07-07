# kn_sock/cli.py

import argparse
import sys
from kn_sock.tcp import send_tcp_message, start_tcp_server
from kn_sock.udp import send_udp_message, start_udp_server
from kn_sock.file_transfer import send_file, start_file_server
from kn_sock.live_stream import start_live_stream, connect_to_live_server


def tcp_echo_handler(data, addr, conn):
    print(f"[TCP][SERVER] Received from {addr}: {data}")
    conn.sendall(b"Echo: " + data)


def udp_echo_handler(data, addr, sock):
    print(f"[UDP][SERVER] Received from {addr}: {data.decode()}")
    sock.sendto(b"Echo: " + data, addr)


def run_cli():
    parser = argparse.ArgumentParser(
        description="kn_sock: Simplified socket utilities"
    )

    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # --------------------------
    # send-tcp
    # --------------------------
    tcp_send = subparsers.add_parser("send-tcp", help="Send a message over TCP")
    tcp_send.add_argument("host", type=str, help="Target host")
    tcp_send.add_argument("port", type=int, help="Target port")
    tcp_send.add_argument("message", type=str, help="Message to send")

    # --------------------------
    # send-udp
    # --------------------------
    udp_send = subparsers.add_parser("send-udp", help="Send a message over UDP")
    udp_send.add_argument("host", type=str, help="Target host")
    udp_send.add_argument("port", type=int, help="Target port")
    udp_send.add_argument("message", type=str, help="Message to send")

    # --------------------------
    # send-file
    # --------------------------
    file_send = subparsers.add_parser("send-file", help="Send file over TCP")
    file_send.add_argument("host", type=str, help="Target host")
    file_send.add_argument("port", type=int, help="Target port")
    file_send.add_argument("filepath", type=str, help="Path to file to send")

    # --------------------------
    # run-tcp-server
    # --------------------------
    tcp_server = subparsers.add_parser("run-tcp-server", help="Start a basic TCP echo server")
    tcp_server.add_argument("port", type=int, help="Port to bind server")

    # --------------------------
    # run-udp-server
    # --------------------------
    udp_server = subparsers.add_parser("run-udp-server", help="Start a basic UDP echo server")
    udp_server.add_argument("port", type=int, help="Port to bind server")

    # --------------------------
    # run-file-server
    # --------------------------
    file_server = subparsers.add_parser("run-file-server", help="Start a TCP file receiver")
    file_server.add_argument("port", type=int, help="Port to bind server")
    file_server.add_argument("save_dir", type=str, help="Directory to save received files")

    # --------------------------
    # run-live-server
    # --------------------------
    live_server = subparsers.add_parser("run-live-server", help="Start a live video/audio stream server")
    live_server.add_argument("port", type=int, help="Port for video stream (audio will use port+1 by default)")
    live_server.add_argument("video_path", type=str, help="Path to video file to stream")
    live_server.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    live_server.add_argument("--audio-port", type=int, default=None, help="Port for audio stream (default: port+1)")

    # --------------------------
    # connect-live-server
    # --------------------------
    live_client = subparsers.add_parser("connect-live-server", help="Connect to a live video/audio stream server")
    live_client.add_argument("ip", type=str, help="Server IP address")
    live_client.add_argument("port", type=int, help="Video port (audio will use port+1 by default)")
    live_client.add_argument("--audio-port", type=int, default=None, help="Audio port (default: port+1)")

    # --------------------------
    # Parse args and run
    # --------------------------
    args = parser.parse_args()

    if args.command == "send-tcp":
        send_tcp_message(args.host, args.port, args.message)

    elif args.command == "send-udp":
        send_udp_message(args.host, args.port, args.message)

    elif args.command == "send-file":
        send_file(args.host, args.port, args.filepath)

    elif args.command == "run-tcp-server":
        start_tcp_server(args.port, tcp_echo_handler)

    elif args.command == "run-udp-server":
        start_udp_server(args.port, udp_echo_handler)

    elif args.command == "run-file-server":
        start_file_server(args.port, args.save_dir)

    elif args.command == "run-live-server":
        start_live_stream(args.port, args.video_path, host=args.host, audio_port=args.audio_port)

    elif args.command == "connect-live-server":
        connect_to_live_server(args.ip, args.port, audio_port=args.audio_port)

    else:
        parser.print_help()
        sys.exit(1)
