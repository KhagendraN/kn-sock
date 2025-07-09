# kn_sock/cli.py

import argparse
import sys
from kn_sock.tcp import send_tcp_message, start_tcp_server, start_ssl_tcp_server, send_ssl_tcp_message
from kn_sock.udp import send_udp_message, start_udp_server
from kn_sock.file_transfer import send_file, start_file_server
from kn_sock.live_stream import start_live_stream, connect_to_live_server
from kn_sock.websocket import start_websocket_server, connect_websocket
from kn_sock.http import http_get, http_post, https_get, https_post, start_http_server
from kn_sock.pubsub import start_pubsub_server, PubSubClient
from kn_sock.rpc import start_rpc_server, RPCClient
import os
import time


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
    live_server.add_argument("video_paths", type=str, nargs='+', help="Path(s) to video file(s) to stream (one or more)")
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
    # run-ssl-tcp-server
    # --------------------------
    ssl_tcp_server = subparsers.add_parser("run-ssl-tcp-server", help="Start a secure SSL/TLS TCP server")
    ssl_tcp_server.add_argument("port", type=int, help="Port to bind server")
    ssl_tcp_server.add_argument("certfile", type=str, help="Path to server certificate (PEM)")
    ssl_tcp_server.add_argument("keyfile", type=str, help="Path to server private key (PEM)")
    ssl_tcp_server.add_argument("--cafile", type=str, default=None, help="CA cert for client cert verification (optional)")
    ssl_tcp_server.add_argument("--require-client-cert", action="store_true", help="Require client certificate (mutual TLS)")
    ssl_tcp_server.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")

    # --------------------------
    # send-ssl-tcp
    # --------------------------
    ssl_tcp_client = subparsers.add_parser("send-ssl-tcp", help="Send a message over SSL/TLS TCP")
    ssl_tcp_client.add_argument("host", type=str, help="Target host")
    ssl_tcp_client.add_argument("port", type=int, help="Target port")
    ssl_tcp_client.add_argument("message", type=str, help="Message to send")
    ssl_tcp_client.add_argument("--cafile", type=str, default=None, help="CA cert for server verification (optional)")
    ssl_tcp_client.add_argument("--certfile", type=str, default=None, help="Client certificate (PEM) for mutual TLS (optional)")
    ssl_tcp_client.add_argument("--keyfile", type=str, default=None, help="Client private key (PEM) for mutual TLS (optional)")
    ssl_tcp_client.add_argument("--no-verify", action="store_true", help="Disable server certificate verification")

    # --------------------------
    # WebSocket Server
    # --------------------------
    ws_server = subparsers.add_parser("run-websocket-server", help="Start a WebSocket echo server")
    ws_server.add_argument("port", type=int, help="Port to bind server")
    ws_server.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")

    # WebSocket Client
    ws_client = subparsers.add_parser("websocket-client", help="Connect to a WebSocket server and send a message")
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
    http_server = subparsers.add_parser("run-http-server", help="Start a minimal HTTP server (static + routes)")
    http_server.add_argument("port", type=int)
    http_server.add_argument("--host", type=str, default="127.0.0.1")
    http_server.add_argument("--static-dir", type=str, default=None)

    # PubSub Server
    pubsub_server = subparsers.add_parser("run-pubsub-server", help="Start a pub/sub server")
    pubsub_server.add_argument("port", type=int)
    pubsub_server.add_argument("--host", type=str, default="127.0.0.1")

    # PubSub Client
    pubsub_client = subparsers.add_parser("pubsub-client", help="Connect to pub/sub server, subscribe, publish, and receive")
    pubsub_client.add_argument("host", type=str)
    pubsub_client.add_argument("port", type=int)
    pubsub_client.add_argument("topic", type=str)
    pubsub_client.add_argument("message", type=str, nargs="?", default=None)

    # RPC Server
    rpc_server = subparsers.add_parser("run-rpc-server", help="Start an RPC server with add/echo")
    rpc_server.add_argument("port", type=int)
    rpc_server.add_argument("--host", type=str, default="127.0.0.1")

    # RPC Client
    rpc_client = subparsers.add_parser("rpc-client", help="Connect to RPC server and call a function")
    rpc_client.add_argument("host", type=str)
    rpc_client.add_argument("port", type=int)
    rpc_client.add_argument("function", type=str)
    rpc_client.add_argument("args", nargs="*", help="Arguments for the function")

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
        start_live_stream(args.port, args.video_paths, host=args.host, audio_port=args.audio_port)

    elif args.command == "connect-live-server":
        connect_to_live_server(args.ip, args.port, audio_port=args.audio_port)

    elif args.command == "run-ssl-tcp-server":
        start_ssl_tcp_server(
            args.port,
            tcp_echo_handler,
            certfile=args.certfile,
            keyfile=args.keyfile,
            cafile=args.cafile,
            require_client_cert=args.require_client_cert,
            host=args.host
        )

    elif args.command == "send-ssl-tcp":
        send_ssl_tcp_message(
            args.host,
            args.port,
            args.message,
            cafile=args.cafile,
            certfile=args.certfile,
            keyfile=args.keyfile,
            verify=not args.no_verify
        )

    elif args.command == "run-websocket-server":
        def echo_handler(ws):
            print(f"[WebSocket][SERVER] Client connected: {ws.addr}")
            try:
                while ws.open:
                    msg = ws.recv()
                    if not msg:
                        break
                    print(f"[WebSocket][SERVER] Received: {msg}")
                    ws.send(f"Echo: {msg}")
            finally:
                ws.close()
                print(f"[WebSocket][SERVER] Client disconnected: {ws.addr}")
        import threading
        shutdown_event = threading.Event()
        server_thread = threading.Thread(
            target=start_websocket_server,
            args=(args.host, args.port, echo_handler),
            kwargs={"shutdown_event": shutdown_event},
            daemon=True
        )
        server_thread.start()
        print("[WebSocket][SERVER] Running. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[WebSocket][SERVER] Shutting down...")
            shutdown_event.set()
            server_thread.join()

    elif args.command == "websocket-client":
        ws = connect_websocket(args.host, args.port)
        print("[WebSocket][CLIENT] Connected to server.")
        ws.send(args.message)
        print(f"[WebSocket][CLIENT] Sent: {args.message}")
        reply = ws.recv()
        print(f"[WebSocket][CLIENT] Received: {reply}")
        ws.close()
        print("[WebSocket][CLIENT] Connection closed.")

    elif args.command == "http-get":
        body = http_get(args.host, args.port, args.path)
        print(body)
    elif args.command == "https-get":
        body = https_get(args.host, args.port, args.path)
        print(body)
    elif args.command == "http-post":
        body = http_post(args.host, args.port, args.path, data=args.data)
        print(body)
    elif args.command == "https-post":
        body = https_post(args.host, args.port, args.path, data=args.data)
        print(body)

    elif args.command == "run-http-server":
        def hello_route(request, client_sock):
            client_sock.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nHello")
        def echo_post(request, client_sock):
            body = request['raw'].split(b'\r\n\r\n', 1)[-1]
            resp = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body
            client_sock.sendall(resp)
        routes = {
            ("GET", "/hello"): hello_route,
            ("POST", "/echo"): echo_post,
        }
        import threading
        shutdown_event = threading.Event()
        server_thread = threading.Thread(
            target=start_http_server,
            args=(args.host, args.port),
            kwargs={"static_dir": args.static_dir, "routes": routes, "shutdown_event": shutdown_event},
            daemon=True
        )
        server_thread.start()
        print("[HTTP][SERVER] Running. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[HTTP][SERVER] Shutting down...")
            shutdown_event.set()
            server_thread.join()

    elif args.command == "run-pubsub-server":
        import threading
        shutdown_event = threading.Event()
        server_thread = threading.Thread(
            target=start_pubsub_server,
            args=(args.port,),
            kwargs={"host": args.host, "shutdown_event": shutdown_event},
            daemon=True
        )
        server_thread.start()
        print("[PubSub][SERVER] Running. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[PubSub][SERVER] Shutting down...")
            shutdown_event.set()
            server_thread.join()

    elif args.command == "pubsub-client":
        client = PubSubClient(args.host, args.port)
        client.subscribe(args.topic)
        print(f"[PubSub][CLIENT] Subscribed to '{args.topic}'")
        if args.message:
            client.publish(args.topic, args.message)
            print(f"[PubSub][CLIENT] Published to '{args.topic}': {args.message}")
        print("[PubSub][CLIENT] Waiting for messages (Ctrl+C to exit)...")
        try:
            while True:
                msg = client.recv(timeout=5)
                if msg:
                    print(f"[PubSub][CLIENT] Received: {msg}")
        except KeyboardInterrupt:
            print("[PubSub][CLIENT] Closing connection.")
            client.close()

    elif args.command == "run-rpc-server":
        def add(a, b):
            return a + b
        def echo(msg):
            return msg
        funcs = {"add": add, "echo": echo}
        import threading
        shutdown_event = threading.Event()
        server_thread = threading.Thread(
            target=start_rpc_server,
            args=(args.port, funcs),
            kwargs={"host": args.host, "shutdown_event": shutdown_event},
            daemon=True
        )
        server_thread.start()
        print("[RPC][SERVER] Running. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[RPC][SERVER] Shutting down...")
            shutdown_event.set()
            server_thread.join()

    elif args.command == "rpc-client":
        client = RPCClient(args.host, args.port)
        try:
            # Try to parse args as ints or floats if possible
            parsed_args = []
            for a in args.args:
                try:
                    parsed_args.append(int(a))
                except ValueError:
                    try:
                        parsed_args.append(float(a))
                    except ValueError:
                        parsed_args.append(a)
            result = client.call(args.function, *parsed_args)
            print(f"[RPC][CLIENT] {args.function}{tuple(parsed_args)} = {result}")
        except Exception as e:
            print(f"[RPC][CLIENT] Error: {e}")
        finally:
            client.close()

    else:
        parser.print_help()
        sys.exit(1)
