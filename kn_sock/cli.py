# kn_sock/cli.py

import argparse
import sys
import logging

print("DEBUG: CLI launched", flush=True)

logger = logging.getLogger("kn_sock.cli")
from kn_sock.tcp import (
    send_tcp_message,
    start_tcp_server,
    start_ssl_tcp_server,
    send_ssl_tcp_message,
)
from kn_sock.udp import send_udp_message, start_udp_server
from kn_sock.file_transfer import send_file, start_file_server
from kn_sock.live_stream import start_live_stream, connect_to_live_server
from kn_sock.websocket import start_websocket_server, connect_websocket
from kn_sock.http import http_get, http_post, https_get, https_post, start_http_server
from kn_sock.pubsub import start_pubsub_server, PubSubClient
from kn_sock.rpc import start_rpc_server, RPCClient
from kn_sock.video_chat import VideoChatServer, VideoChatClient
import os
import time
from kn_sock import interactive_cli


def tcp_echo_handler(data, addr, conn):
    logger.info(f"[TCP][SERVER] Received from {addr}: {data}")
    conn.sendall(b"Echo: " + data)


def udp_echo_handler(data, addr, sock):
    logger.info(f"[UDP][SERVER] Received from {addr}: {data.decode()}")
    sock.sendto(b"Echo: " + data, addr)


def run_cli():
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s][%(name)s] %(message)s", force=True
    )
    parser = argparse.ArgumentParser(description="kn_sock: Simplified socket utilities")

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
    tcp_server = subparsers.add_parser(
        "run-tcp-server", help="Start a basic TCP echo server"
    )
    tcp_server.add_argument("port", type=int, help="Port to bind server")

    # --------------------------
    # run-udp-server
    # --------------------------
    udp_server = subparsers.add_parser(
        "run-udp-server", help="Start a basic UDP echo server"
    )
    udp_server.add_argument("port", type=int, help="Port to bind server")

    # --------------------------
    # run-file-server
    # --------------------------
    file_server = subparsers.add_parser(
        "run-file-server", help="Start a TCP file receiver"
    )
    file_server.add_argument("port", type=int, help="Port to bind server")
    file_server.add_argument(
        "save_dir", type=str, help="Directory to save received files"
    )

    # --------------------------
    # run-live-server
    # --------------------------
    live_server = subparsers.add_parser(
        "run-live-server", help="Start a live video/audio stream server"
    )
    live_server.add_argument(
        "port",
        type=int,
        help="Port for video stream (audio will use port+1 by default)",
    )
    live_server.add_argument(
        "video_paths",
        type=str,
        nargs="+",
        help="Path(s) to video file(s) to stream (one or more)",
    )
    live_server.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)"
    )
    live_server.add_argument(
        "--audio-port",
        type=int,
        default=None,
        help="Port for audio stream (default: port+1)",
    )

    # --------------------------
    # connect-live-server
    # --------------------------
    live_client = subparsers.add_parser(
        "connect-live-server", help="Connect to a live video/audio stream server"
    )
    live_client.add_argument("ip", type=str, help="Server IP address")
    live_client.add_argument(
        "port", type=int, help="Video port (audio will use port+1 by default)"
    )
    live_client.add_argument(
        "--audio-port", type=int, default=None, help="Audio port (default: port+1)"
    )

    # --------------------------
    # run-video-chat-server
    # --------------------------
    video_chat_server = subparsers.add_parser(
        "run-video-chat-server", help="Start a multi-client video chat server"
    )
    video_chat_server.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)"
    )
    video_chat_server.add_argument(
        "--video-port",
        type=int,
        default=9000,
        help="Port for video stream (default: 9000)",
    )
    video_chat_server.add_argument(
        "--audio-port",
        type=int,
        default=9001,
        help="Port for audio stream (default: 9001)",
    )
    video_chat_server.add_argument(
        "--text-port", type=int, default=9002, help="Port for text chat (default: 9002)"
    )

    # --------------------------
    # connect-video-chat
    # --------------------------
    video_chat_client = subparsers.add_parser(
        "connect-video-chat", help="Connect to a video chat server"
    )
    video_chat_client.add_argument("server_ip", type=str, help="Server IP address")
    video_chat_client.add_argument("room", type=str, help="Room name to join")
    video_chat_client.add_argument("nickname", type=str, help="Your nickname")
    video_chat_client.add_argument(
        "--video-port", type=int, default=9000, help="Video port (default: 9000)"
    )
    video_chat_client.add_argument(
        "--audio-port", type=int, default=9001, help="Audio port (default: 9001)"
    )
    video_chat_client.add_argument(
        "--text-port", type=int, default=9002, help="Text port (default: 9002)"
    )

    # --------------------------
    # run-ssl-tcp-server
    # --------------------------
    ssl_tcp_server = subparsers.add_parser(
        "run-ssl-tcp-server", help="Start a secure SSL/TLS TCP server"
    )
    ssl_tcp_server.add_argument("port", type=int, help="Port to bind server")
    ssl_tcp_server.add_argument(
        "certfile", type=str, help="Path to server certificate (PEM)"
    )
    ssl_tcp_server.add_argument(
        "keyfile", type=str, help="Path to server private key (PEM)"
    )
    ssl_tcp_server.add_argument(
        "--cafile",
        type=str,
        default=None,
        help="CA cert for client cert verification (optional)",
    )
    ssl_tcp_server.add_argument(
        "--require-client-cert",
        action="store_true",
        help="Require client certificate (mutual TLS)",
    )
    ssl_tcp_server.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)"
    )

    # --------------------------
    # send-ssl-tcp
    # --------------------------
    ssl_tcp_client = subparsers.add_parser(
        "send-ssl-tcp", help="Send a message over SSL/TLS TCP"
    )
    ssl_tcp_client.add_argument("host", type=str, help="Target host")
    ssl_tcp_client.add_argument("port", type=int, help="Target port")
    ssl_tcp_client.add_argument("message", type=str, help="Message to send")
    ssl_tcp_client.add_argument(
        "--cafile",
        type=str,
        default=None,
        help="CA cert for server verification (optional)",
    )
    ssl_tcp_client.add_argument(
        "--certfile",
        type=str,
        default=None,
        help="Client certificate (PEM) for mutual TLS (optional)",
    )
    ssl_tcp_client.add_argument(
        "--keyfile",
        type=str,
        default=None,
        help="Client private key (PEM) for mutual TLS (optional)",
    )
    ssl_tcp_client.add_argument(
        "--no-verify",
        action="store_true",
        help="Disable server certificate verification",
    )

    # --------------------------
    # WebSocket Server
    # --------------------------
    ws_server = subparsers.add_parser(
        "run-websocket-server", help="Start a WebSocket echo server"
    )
    ws_server.add_argument("port", type=int, help="Port to bind server")
    ws_server.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind (default: 127.0.0.1)",
    )

    # WebSocket Client
    ws_client = subparsers.add_parser(
        "websocket-client", help="Connect to a WebSocket server and send a message"
    )
    ws_client.add_argument("host", type=str, help="Server host")
    ws_client.add_argument("port", type=int, help="Server port")
    ws_client.add_argument("message", type=str, help="Message to send")

    # HTTP/HTTPS Client
    http_get_cmd = subparsers.add_parser("http-get", help="HTTP GET request")
    http_get_cmd.add_argument("host", type=str)
    http_get_cmd.add_argument("port", type=int)
    http_get_cmd.add_argument("path", type=str, default="/", nargs="?")
    https_get_cmd = subparsers.add_parser("https-get", help="HTTPS GET request")
    https_get_cmd.add_argument("host", type=str)
    https_get_cmd.add_argument("port", type=int)
    https_get_cmd.add_argument("path", type=str, default="/", nargs="?")
    http_post_cmd = subparsers.add_parser("http-post", help="HTTP POST request")
    http_post_cmd.add_argument("host", type=str)
    http_post_cmd.add_argument("port", type=int)
    http_post_cmd.add_argument("path", type=str, default="/", nargs="?")
    http_post_cmd.add_argument("data", type=str, default="")
    https_post_cmd = subparsers.add_parser("https-post", help="HTTPS POST request")
    https_post_cmd.add_argument("host", type=str)
    https_post_cmd.add_argument("port", type=int)
    https_post_cmd.add_argument("path", type=str, default="/", nargs="?")
    https_post_cmd.add_argument("data", type=str, default="")

    # HTTP Server
    http_server = subparsers.add_parser(
        "run-http-server", help="Start a minimal HTTP server (static + routes)"
    )
    http_server.add_argument("port", type=int)
    http_server.add_argument("--host", type=str, default="127.0.0.1")
    http_server.add_argument("--static-dir", type=str, default=None)

    # PubSub Server
    pubsub_server = subparsers.add_parser(
        "run-pubsub-server", help="Start a pub/sub server"
    )
    pubsub_server.add_argument("port", type=int)
    pubsub_server.add_argument("--host", type=str, default="127.0.0.1")

    # PubSub Client
    pubsub_client = subparsers.add_parser(
        "pubsub-client",
        help="Connect to pub/sub server, subscribe, publish, and receive",
    )
    pubsub_client.add_argument("host", type=str)
    pubsub_client.add_argument("port", type=int)
    pubsub_client.add_argument("topic", type=str)
    pubsub_client.add_argument("message", type=str, nargs="?", default=None)

    # RPC Server
    rpc_server = subparsers.add_parser(
        "run-rpc-server", help="Start an RPC server with add/echo"
    )
    rpc_server.add_argument("port", type=int)
    rpc_server.add_argument("--host", type=str, default="127.0.0.1")

    # RPC Client
    rpc_client = subparsers.add_parser(
        "rpc-client", help="Connect to RPC server and call a function"
    )
    rpc_client.add_argument("host", type=str)
    rpc_client.add_argument("port", type=int)
    rpc_client.add_argument("function", type=str)
    rpc_client.add_argument("args", nargs="*", help="Arguments for the function")

    # Interactive CLI subcommand
    subparsers.add_parser("interactive", help="Start the interactive kn-sock CLI")

    # --------------------------
    # Parse args and run
    # --------------------------
    args = parser.parse_args()

    # --- Validation helpers ---
    import re

    def is_valid_port(port):
        return isinstance(port, int) and 1 <= port <= 65535

    def is_valid_host(host):
        # Accepts IPv4, IPv6, or DNS names (basic check)
        if not isinstance(host, str):
            return False
        if host in ("localhost", "0.0.0.0", "127.0.0.1", "::1"):
            return True
        ipv4 = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        ipv6 = re.compile(r"^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$")
        dns = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$")
        return bool(ipv4.match(host) or ipv6.match(host) or dns.match(host))

    def is_valid_file(path):
        return os.path.isfile(path)

    def is_valid_dir(path):
        return os.path.isdir(path)

    def error_exit(msg):
        logger.error(f"[ERROR] {msg}")
        sys.exit(2)

    # --- Validate arguments for each command ---
    if args.command in [
        "send-tcp",
        "send-udp",
        "send-file",
        "send-ssl-tcp",
        "websocket-client",
        "http-get",
        "https-get",
        "http-post",
        "https-post",
        "pubsub-client",
        "rpc-client",
    ]:
        if hasattr(args, "host") and not is_valid_host(args.host):
            error_exit(f"Invalid host: {args.host}")
        if hasattr(args, "port") and not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
    if args.command == "send-file":
        if not is_valid_file(args.filepath):
            error_exit(f"File not found: {args.filepath}")
    if (
        args.command == "run-tcp-server"
        or args.command == "run-udp-server"
        or args.command == "run-file-server"
    ):
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
    if args.command == "run-file-server":
        if not is_valid_dir(args.save_dir):
            error_exit(f"Directory not found: {args.save_dir}")
    if args.command == "run-live-server":
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
        for path in args.video_paths:
            if not is_valid_file(path):
                error_exit(f"Video file not found: {path}")
        if args.audio_port is not None and not is_valid_port(args.audio_port):
            error_exit(f"Invalid audio port: {args.audio_port} (must be 1-65535)")
        if hasattr(args, "host") and not is_valid_host(args.host):
            error_exit(f"Invalid host: {args.host}")
    if args.command == "connect-live-server":
        if not is_valid_host(args.ip):
            error_exit(f"Invalid server IP: {args.ip}")
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
        if args.audio_port is not None and not is_valid_port(args.audio_port):
            error_exit(f"Invalid audio port: {args.audio_port} (must be 1-65535)")
    if args.command == "run-video-chat-server":
        if not is_valid_host(args.host):
            error_exit(f"Invalid host: {args.host}")
        for p in [args.video_port, args.audio_port, args.text_port]:
            if not is_valid_port(p):
                error_exit(f"Invalid port: {p} (must be 1-65535)")
    if args.command == "connect-video-chat":
        if not is_valid_host(args.server_ip):
            error_exit(f"Invalid server IP: {args.server_ip}")
        for p in [args.video_port, args.audio_port, args.text_port]:
            if not is_valid_port(p):
                error_exit(f"Invalid port: {p} (must be 1-65535)")
    if args.command == "run-ssl-tcp-server":
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
        for f in [args.certfile, args.keyfile]:
            if not is_valid_file(f):
                error_exit(f"File not found: {f}")
        if args.cafile and not is_valid_file(args.cafile):
            error_exit(f"CA file not found: {args.cafile}")
        if hasattr(args, "host") and not is_valid_host(args.host):
            error_exit(f"Invalid host: {args.host}")
    if args.command == "send-ssl-tcp":
        if args.cafile and not is_valid_file(args.cafile):
            error_exit(f"CA file not found: {args.cafile}")
        if args.certfile and not is_valid_file(args.certfile):
            error_exit(f"Client certificate not found: {args.certfile}")
        if args.keyfile and not is_valid_file(args.keyfile):
            error_exit(f"Client key not found: {args.keyfile}")
    if args.command == "run-websocket-server":
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
        if hasattr(args, "host") and not is_valid_host(args.host):
            error_exit(f"Invalid host: {args.host}")
    if (
        args.command == "http-get"
        or args.command == "https-get"
        or args.command == "http-post"
        or args.command == "https-post"
    ):
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
    if args.command == "run-http-server":
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
        if hasattr(args, "host") and not is_valid_host(args.host):
            error_exit(f"Invalid host: {args.host}")
        if args.static_dir and not is_valid_dir(args.static_dir):
            error_exit(f"Static directory not found: {args.static_dir}")
    if args.command == "run-pubsub-server":
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
        if hasattr(args, "host") and not is_valid_host(args.host):
            error_exit(f"Invalid host: {args.host}")
    if args.command == "pubsub-client":
        if not is_valid_host(args.host):
            error_exit(f"Invalid host: {args.host}")
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
    if args.command == "run-rpc-server":
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")
        if hasattr(args, "host") and not is_valid_host(args.host):
            error_exit(f"Invalid host: {args.host}")
    if args.command == "rpc-client":
        if not is_valid_host(args.host):
            error_exit(f"Invalid host: {args.host}")
        if not is_valid_port(args.port):
            error_exit(f"Invalid port: {args.port} (must be 1-65535)")

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
        start_live_stream(
            args.port, args.video_paths, host=args.host, audio_port=args.audio_port
        )

    elif args.command == "connect-live-server":
        connect_to_live_server(args.ip, args.port, audio_port=args.audio_port)

    elif args.command == "run-video-chat-server":
        server = VideoChatServer(
            host=args.host,
            video_port=args.video_port,
            audio_port=args.audio_port,
            text_port=args.text_port,
        )
        logger.info(f"Video chat server started on ports:")
        logger.info(f"  - {args.video_port} (video)")
        logger.info(f"  - {args.audio_port} (audio)")
        logger.info(f"  - {args.text_port} (text chat)")
        logger.info(
            "Features: video/audio chat, text messaging, mute/unmute, video on/off"
        )
        server.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Server stopped.")

    elif args.command == "connect-video-chat":
        client = VideoChatClient(
            server_ip=args.server_ip,
            video_port=args.video_port,
            audio_port=args.audio_port,
            text_port=args.text_port,
            room=args.room,
            nickname=args.nickname,
        )
        logger.info(
            f"Connecting to video chat server at {args.server_ip}:{args.video_port}/{args.audio_port}/{args.text_port}"
        )
        logger.info(f'Room: "{args.room}", Nickname: "{args.nickname}"')
        logger.info('Controls: "m" to mute/unmute, "v" to toggle video, "q" to quit')
        client.start()
        try:
            while client.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Client stopped.")

    elif args.command == "run-ssl-tcp-server":
        start_ssl_tcp_server(
            args.port,
            tcp_echo_handler,
            args.certfile,
            args.keyfile,
            cafile=args.cafile,
            require_client_cert=args.require_client_cert,
            host=args.host,
        )

    elif args.command == "send-ssl-tcp":
        send_ssl_tcp_message(
            args.host,
            args.port,
            args.message,
            cafile=args.cafile,
            certfile=args.certfile,
            keyfile=args.keyfile,
            verify=not args.no_verify,
        )

    elif args.command == "run-websocket-server":

        def echo_handler(ws):
            logger.info(f"[WebSocket][SERVER] Client connected: {ws.addr}")
            try:
                while ws.open:
                    msg = ws.recv()
                    if not msg:
                        break
                    ws.send(f"Echo: {msg}")
            finally:
                ws.close()
                logger.info(f"[WebSocket][SERVER] Client disconnected: {ws.addr}")

        start_websocket_server(args.host, args.port, echo_handler)

    elif args.command == "websocket-client":
        ws = connect_websocket(args.host, args.port)
        ws.send(args.message)
        reply = ws.recv()
        logger.info(f"Received: {reply}")
        ws.close()

    elif args.command == "http-get":
        body = http_get(args.host, args.port, args.path)
        logger.info(body)

    elif args.command == "https-get":
        body = https_get(args.host, args.port, args.path)
        logger.info(body)

    elif args.command == "http-post":
        body = http_post(args.host, args.port, args.path, args.data)
        logger.info(body)

    elif args.command == "https-post":
        body = https_post(args.host, args.port, args.path, args.data)
        logger.info(body)

    elif args.command == "run-http-server":

        def hello_route(request, client_sock):
            client_sock.send(
                b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, World!"
            )

        def echo_post(request, client_sock):
            client_sock.send(
                b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nEcho: "
                + request.split(b"\r\n\r\n", 1)[1]
            )

        routes = {"/hello": hello_route, "/echo": echo_post}
        start_http_server(
            args.host, args.port, static_dir=args.static_dir, routes=routes
        )

    elif args.command == "run-pubsub-server":
        start_pubsub_server(args.port, host=args.host)

    elif args.command == "pubsub-client":
        client = PubSubClient(args.host, args.port)
        client.subscribe(args.topic)
        if args.message:
            client.publish(args.topic, args.message)
        msg = client.recv(timeout=2)
        logger.info(msg)
        client.close()

    elif args.command == "run-rpc-server":

        def add(a, b):
            return a + b

        def echo(msg):
            return msg

        funcs = {"add": add, "echo": echo}
        start_rpc_server(args.port, funcs, host=args.host)

    elif args.command == "rpc-client":
        client = RPCClient(args.host, args.port)
        result = client.call(args.function, *args.args)
        logger.info(result)
        client.close()

    elif args.command == "interactive":
        interactive_cli.KnSockInteractiveCLI().cmdloop()

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    run_cli()
