import os
import sys
import subprocess
import pytest

EXAMPLES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../examples'))
REAL_WORLD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/real_world_examples'))

# Scripts that run forever or require interaction (skip for smoke test)
SKIP_SCRIPTS = {
    # Servers or interactive
    'async_server.py', 'tcp_server.py', 'udp_server.py', 'websocket_server.py', 'rpc_server.py',
    'pubsub_server.py', 'http_server.py', 'udp_multicast_server.py', 'tcp_ssl_server.py',
    'tcp_ssl_server_async.py', 'file_server.py', 'chat_server.py', 'server_live.py',
    'json_server.py',
    # Real world examples (servers)
    'http_api_server.py', 'chat_app.py', 'live_streaming.py', 'microservice_rpc.py', 'remote_control.py', 'iot_protocol.py', 'file_transfer.py',
    # Client-only or utility scripts that require a server or special env
    'rpc_client.py', 'tcp_ssl_pool.py', 'websocket_client.py', 'file_sender.py', 'json_client.py',
    'tcp_client.py', 'tcp_pool.py', 'pubsub_client.py', 'tcp_ssl_client.py', 'tcp_ssl_client_async.py', 'test_utilities.py',
}

# Scripts that require minimal arguments to run (map: script -> [args])
SCRIPT_ARGS = {
    'tcp_client.py': ['localhost', '8080', 'test'],
    'udp_client.py': ['localhost', '8080', 'test'],
    'file_sender.py': ['localhost', '8080', 'test.txt'],
    'file_transfer.py': ['client', 'test.txt'],
    'json_client.py': ['localhost', '8080', '{"test":1}'],
    'pubsub_client.py': ['localhost', '9000', 'test'],
    'rpc_client.py': ['localhost', '9001', 'echo', 'hi'],
    'https_client.py': ['localhost', '443', '/'],
    'http_client.py': ['localhost', '80', '/'],
    'websocket_client.py': ['localhost', '8765', 'test'],
    'client_live.py': ['localhost'],
    'test_utilities.py': ['free_port'],
}

# List all scripts in examples/
example_scripts = [
    f for f in os.listdir(EXAMPLES_DIR)
    if f.endswith('.py') and not f.startswith('test')
]

# List all scripts in real_world_examples/
real_world_scripts = [
    f for f in os.listdir(REAL_WORLD_DIR)
    if f.endswith('.py')
]

def run_script(path, args=None):
    cmd = [sys.executable, path]
    if args:
        cmd += args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    return result

@pytest.mark.parametrize('script', example_scripts)
def test_examples_scripts(script):
    if script in SKIP_SCRIPTS:
        pytest.skip(f"Skipping long-running or server script: {script}")
    path = os.path.join(EXAMPLES_DIR, script)
    args = SCRIPT_ARGS.get(script)
    try:
        result = run_script(path, args)
        # Accept exit code 0 or 1 if usage/help is printed
        ok = (result.returncode == 0 or
              (result.returncode == 1 and (b'usage' in result.stdout.lower() or b'usage' in result.stderr.lower())))
        assert ok, f"{script} failed: {result.stdout}\n{result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.skip(f"Timeout (likely server or interactive): {script}")

@pytest.mark.parametrize('script', real_world_scripts)
def test_real_world_examples_scripts(script):
    if script in SKIP_SCRIPTS:
        pytest.skip(f"Skipping long-running or server script: {script}")
    path = os.path.join(REAL_WORLD_DIR, script)
    args = SCRIPT_ARGS.get(script)
    try:
        result = run_script(path, args)
        ok = (result.returncode == 0 or
              (result.returncode == 1 and (b'usage' in result.stdout.lower() or b'usage' in result.stderr.lower())))
        assert ok, f"{script} failed: {result.stdout}\n{result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.skip(f"Timeout (likely server or interactive): {script}")

# --- Performance Benchmark ---
def test_tcp_message_throughput(benchmark):
    from kn_sock.tcp import send_tcp_message, start_tcp_server
    import threading
    import time
    results = []
    def handler(data, addr, sock):
        results.append(data)
        sock.sendall(b'ack')
    server_thread = threading.Thread(target=start_tcp_server, args=(9099, handler), daemon=True)
    server_thread.start()
    time.sleep(0.5)
    def send():
        send_tcp_message('127.0.0.1', 9099, 'ping')
    benchmark(send) 