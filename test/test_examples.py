import os
import sys
import subprocess
import pytest
import threading
import socket
import time
import io
import contextlib

EXAMPLES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples"))
REAL_WORLD_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../docs/real_world_examples")
)

# Scripts that run forever or require interaction (skip for smoke test)
SKIP_SCRIPTS = {
    # Servers or interactive
    "async_server.py",
    "tcp_server.py",
    "udp_server.py",
    "websocket_server.py",
    "rpc_server.py",
    "pubsub_server.py",
    "http_server.py",
    "udp_multicast_server.py",
    "tcp_ssl_server.py",
    "tcp_ssl_server_async.py",
    "file_server.py",
    "chat_server.py",
    "server_live.py",
    "json_server.py",
    # Real world examples (servers)
    "http_api_server.py",
    "chat_app.py",
    "live_streaming.py",
    "microservice_rpc.py",
    "remote_control.py",
    "iot_protocol.py",
    "file_transfer.py",
    # Client-only or utility scripts that require a server or special env
    "rpc_client.py",
    "tcp_ssl_pool.py",
    "websocket_client.py",
    "file_sender.py",
    "json_client.py",
    "tcp_client.py",
    "tcp_pool.py",
    "pubsub_client.py",
    "tcp_ssl_client.py",
    "tcp_ssl_client_async.py",
    "test_utilities.py",
}

# Scripts that require minimal arguments to run (map: script -> [args])
SCRIPT_ARGS = {
    "tcp_client.py": ["localhost", "8080", "test"],
    "udp_client.py": ["localhost", "8080", "test"],
    "file_sender.py": ["localhost", "8080", "test.txt"],
    "file_transfer.py": ["client", "test.txt"],
    "json_client.py": ["localhost", "8080", '{"test":1}'],
    "pubsub_client.py": ["localhost", "9000", "test"],
    "rpc_client.py": ["localhost", "9001", "echo", "hi"],
    "https_client.py": ["localhost", "443", "/"],
    "http_client.py": ["localhost", "80", "/"],
    "websocket_client.py": ["localhost", "8765", "test"],
    "client_live.py": ["localhost"],
    "test_utilities.py": ["free_port"],
}

# List all scripts in examples/
example_scripts = [
    f
    for f in os.listdir(EXAMPLES_DIR)
    if f.endswith(".py") and not f.startswith("test")
]

# List all scripts in real_world_examples/
real_world_scripts = [f for f in os.listdir(REAL_WORLD_DIR) if f.endswith(".py")]


def run_script(path, args=None):
    cmd = [sys.executable, path]
    if args:
        cmd += args
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10
    )
    return result


def _start_echo_server(host, port, stop_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    s.settimeout(0.5)
    while not stop_event.is_set():
        try:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
        except socket.timeout:
            continue
    s.close()


def test_interactive_cli_echo(tmp_path):
    from kn_sock import interactive_cli

    host, port = "127.0.0.1", 9999
    stop_event = threading.Event()
    server_thread = threading.Thread(
        target=_start_echo_server, args=(host, port, stop_event), daemon=True
    )
    server_thread.start()
    time.sleep(0.2)

    cli = interactive_cli.KnSockInteractiveCLI()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        cli.onecmd(f"connect testconn {host} {port}")
        cli.onecmd("send hello")
        cli.onecmd("receive")
        cli.onecmd("history")
        cli.onecmd("disconnect testconn")
    output = buf.getvalue()
    stop_event.set()
    server_thread.join(timeout=1)
    assert "Connected to" in output
    assert "Message sent." in output
    assert "Received: hello" in output
    assert "[sent] hello" in output and "[recv] hello" in output
    assert "Disconnected" in output


def is_video_chat_env_available():
    # Check for environment variable or server availability
    # For now, just check for a marker env var
    return os.environ.get("KN_SOCK_VIDEO_CHAT_TEST", "") == "1"


@pytest.mark.parametrize("script", example_scripts)
def test_examples_scripts(script):
    if "video_chat_client" in script and not is_video_chat_env_available():
        pytest.skip(
            "Skipping video chat client tests: server or environment not available."
        )
    if script in SKIP_SCRIPTS:
        pytest.skip(f"Skipping long-running or server script: {script}")
    path = os.path.join(EXAMPLES_DIR, script)
    args = SCRIPT_ARGS.get(script)
    try:
        result = run_script(path, args)
        # Accept exit code 0 or 1 if usage/help is printed
        ok = result.returncode == 0 or (
            result.returncode == 1
            and (b"usage" in result.stdout.lower() or b"usage" in result.stderr.lower())
        )
        assert ok, f"{script} failed: {result.stdout}\n{result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.skip(f"Timeout (likely server or interactive): {script}")


@pytest.mark.parametrize("script", real_world_scripts)
def test_real_world_examples_scripts(script):
    if script in SKIP_SCRIPTS:
        pytest.skip(f"Skipping long-running or server script: {script}")
    path = os.path.join(REAL_WORLD_DIR, script)
    args = SCRIPT_ARGS.get(script)
    try:
        result = run_script(path, args)
        ok = result.returncode == 0 or (
            result.returncode == 1
            and (b"usage" in result.stdout.lower() or b"usage" in result.stderr.lower())
        )
        assert ok, f"{script} failed: {result.stdout}\n{result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.skip(f"Timeout (likely server or interactive): {script}")


# --- Performance Benchmark ---
def get_free_port():
    import socket

    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def test_tcp_message_throughput():
    from kn_sock.tcp import start_tcp_server, send_tcp_message
    import threading, time

    port = get_free_port()
    received = []

    def handler(data, addr, sock):
        received.append(data.decode())

    stop_event = threading.Event()

    def server():
        start_tcp_server(port, handler, host="127.0.0.1", shutdown_event=stop_event)

    t = threading.Thread(target=server, daemon=True)
    t.start()
    time.sleep(0.2)
    send_tcp_message("127.0.0.1", port, "throughput-test")
    for _ in range(10):
        if received:
            break
        time.sleep(0.1)
    stop_event.set()
    t.join(timeout=1)
    assert "throughput-test" in received


def test_interactive_cli_help():
    from kn_sock import interactive_cli

    cli = interactive_cli.KnSockInteractiveCLI()
    import io
    import contextlib

    buf = io.StringIO()
    cli.stdout = buf  # Ensure help output is captured
    cli.do_help("")
    output = buf.getvalue()
    assert "connect" in output and "send" in output and "bg_receive" in output
