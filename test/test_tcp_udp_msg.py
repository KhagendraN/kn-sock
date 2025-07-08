import pytest
import asyncio
import threading
import socket
from kn_sock import (
    start_tcp_server, send_tcp_message,
    start_async_tcp_server, send_tcp_message_async,
    start_udp_server, send_udp_message,
    start_udp_server_async, send_udp_message_async,
)
from kn_sock.utils import get_free_port

# --- Sync TCP ---

@pytest.fixture
def run_sync_tcp_server():
    received_messages = []

    def handler(data, addr, client_socket):
        received_messages.append(data.decode())
        client_socket.sendall(b"Message received")

    port = get_free_port()
    server_thread = threading.Thread(target=start_tcp_server, args=(port, handler), daemon=True)
    server_thread.start()

    import time; time.sleep(1)
    yield received_messages, port

def test_sync_tcp(run_sync_tcp_server):
    import time
    received_messages, port = run_sync_tcp_server
    for _ in range(10):
        try:
            send_tcp_message("localhost", port, "Hello, Sync TCP!")
            break
        except ConnectionRefusedError:
            time.sleep(0.2)
    else:
        pytest.fail("TCP server did not start in time")
    time.sleep(0.5)
    assert "Hello, Sync TCP!" in received_messages, (
        "FAILURE: Sync TCP server did NOT receive the expected message."
    )
    print("SUCCESS: Sync TCP server received the expected message.")

# --- Async TCP ---

@pytest.mark.asyncio
async def test_async_tcp():
    received_messages = []

    async def handler(data, addr, writer):
        received_messages.append(data.decode())
        writer.write(b"Message received")
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    server_task = asyncio.create_task(start_async_tcp_server(9091, handler))
    await asyncio.sleep(1)  # wait for server to start

    await send_tcp_message_async("localhost", 9091, "Hello, Async TCP!")

    await asyncio.sleep(1)  # wait for message handling

    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

    assert "Hello, Async TCP!" in received_messages, (
        "FAILURE: Async TCP server did NOT receive the expected message."
    )
    print("SUCCESS: Async TCP server received the expected message.")

# --- Sync UDP ---

@pytest.fixture
def run_sync_udp_server():
    received_messages = []

    def handler(data, addr, server_socket):
        received_messages.append(data.decode())

    server_thread = threading.Thread(target=start_udp_server, args=(9092, handler), daemon=True)
    server_thread.start()

    import time; time.sleep(0.5)
    yield received_messages

def test_sync_udp(run_sync_udp_server):
    send_udp_message("localhost", 9092, "Hello, Sync UDP!")
    import time; time.sleep(0.5)
    assert "Hello, Sync UDP!" in run_sync_udp_server, (
        "FAILURE: Sync UDP server did NOT receive the expected message."
    )
    print("SUCCESS: Sync UDP server received the expected message.")

# --- Async UDP ---

@pytest.mark.asyncio
async def test_async_udp():
    port = get_free_port()
    received_messages = []

    async def handler(data, addr, transport):
        print(f"[TEST][UDP][ASYNC] Handler received: {data}")
        received_messages.append(data.decode())

    server_task = asyncio.create_task(start_udp_server_async(port, handler))
    await asyncio.sleep(3)  # wait for server to start

    await send_udp_message_async("localhost", port, "Hello, Async UDP!")

    await asyncio.sleep(3)  # wait for message handling

    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

    print(f"[TEST][UDP][ASYNC] received_messages: {received_messages}")
    assert "Hello, Async UDP!" in received_messages, (
        "FAILURE: Async UDP server did NOT receive the expected message."
    )
    print("SUCCESS: Async UDP server received the expected message.")

@pytest.mark.asyncio
async def test_async_tcp_server_graceful_shutdown():
    shutdown_event = asyncio.Event()
    async def handler(data, addr, writer):
        pass
    port = get_free_port()
    server_task = asyncio.create_task(start_async_tcp_server(port, handler, shutdown_event=shutdown_event))
    await asyncio.sleep(1)
    shutdown_event.set()
    await asyncio.wait_for(server_task, timeout=2)
    print("[SUCCESS] Async TCP server graceful shutdown")

def test_tcp_server_graceful_shutdown():
    import threading
    import time
    shutdown_event = threading.Event()
    def handler(data, addr, client_socket):
        pass
    server_thread = threading.Thread(
        target=start_tcp_server,
        args=(get_free_port(), handler),
        kwargs={"shutdown_event": shutdown_event},
        daemon=True
    )
    server_thread.start()
    time.sleep(1)
    shutdown_event.set()
    server_thread.join(timeout=2)
    assert not server_thread.is_alive(), "TCP server did not shut down gracefully"
    print("[SUCCESS] TCP server graceful shutdown")

@pytest.mark.asyncio
async def test_async_udp_server_graceful_shutdown():
    shutdown_event = asyncio.Event()
    async def handler(data, addr, transport):
        pass
    port = get_free_port()
    server_task = asyncio.create_task(start_udp_server_async(port, handler, shutdown_event=shutdown_event))
    await asyncio.sleep(1)
    shutdown_event.set()
    await asyncio.wait_for(server_task, timeout=2)
    print("[SUCCESS] Async UDP server graceful shutdown")

def test_tcp_connection_pool():
    from kn_sock import TCPConnectionPool
    import threading
    import time
    port = get_free_port()
    def echo_server():
        def handler(data, addr, client_socket):
            client_socket.sendall(b"ECHO:" + data)
        start_tcp_server(port, handler)
    server_thread = threading.Thread(target=echo_server, daemon=True)
    server_thread.start()
    time.sleep(1)
    pool = TCPConnectionPool('localhost', port, max_size=2, idle_timeout=5)
    with pool.connection() as conn:
        conn.sendall(b"pool test")
        data = conn.recv(1024)
        assert data == b"ECHO:pool test"
    pool.closeall()
    print("[SUCCESS] TCPConnectionPool plain TCP")

@pytest.mark.skipif(not socket.has_ipv6, reason='IPv6 not supported on this platform')
def test_tcp_ipv6():
    import threading
    import time
    received = {}
    def handler(data, addr, client_socket):
        received['data'] = data
        client_socket.sendall(b'ACK:' + data)
    shutdown_event = threading.Event()
    port = get_free_port()
    server_thread = threading.Thread(
        target=start_tcp_server,
        args=(port, handler),
        kwargs={"host": "::1", "shutdown_event": shutdown_event},
        daemon=True
    )
    server_thread.start()
    time.sleep(1)
    send_tcp_message("::1", port, "hello ipv6")
    time.sleep(0.5)
    shutdown_event.set()
    server_thread.join()
    assert received['data'] == b'hello ipv6'
    print("[SUCCESS] IPv6 TCP server/client")

@pytest.mark.skipif(not hasattr(socket, 'IP_ADD_MEMBERSHIP'), reason='Multicast not supported on this platform')
def test_udp_multicast():
    import threading
    import time
    from kn_sock import send_udp_multicast, start_udp_multicast_server
    group = '224.0.0.1'
    port = get_free_port()
    received = {}
    def handler(data, addr, sock):
        received['data'] = data
    shutdown_event = threading.Event()
    server_thread = threading.Thread(
        target=start_udp_multicast_server,
        args=(group, port, handler),
        kwargs={"shutdown_event": shutdown_event},
        daemon=True
    )
    server_thread.start()
    time.sleep(1)
    send_udp_multicast(group, port, "hello multicast")
    time.sleep(1)
    shutdown_event.set()
    server_thread.join()
    assert received['data'] == b'hello multicast'
    print("[SUCCESS] UDP multicast send/receive")

def test_websocket_echo():
    import threading
    import time
    from kn_sock import start_websocket_server, connect_websocket
    received = {}
    def echo_handler(ws):
        msg = ws.recv()
        ws.send(msg)
        ws.close()
    shutdown_event = threading.Event()
    import socket
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    server_thread = threading.Thread(
        target=start_websocket_server,
        args=("127.0.0.1", port, echo_handler),
        kwargs={"shutdown_event": shutdown_event},
        daemon=True
    )
    server_thread.start()
    time.sleep(1)
    ws = connect_websocket("127.0.0.1", port)
    ws.send("test123")
    reply = ws.recv()
    ws.close()
    shutdown_event.set()
    server_thread.join()
    assert reply == "test123"
    print("[SUCCESS] WebSocket echo test")

def test_http_get_post():
    import threading
    import time
    from kn_sock import http_get, http_post
    import http.server
    import socketserver
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"hello get")
        def do_POST(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"hello post")
    with socketserver.TCPServer(("127.0.0.1", 0), Handler) as httpd:
        port = httpd.server_address[1]
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()
        time.sleep(0.5)
        body = http_get("127.0.0.1", port, "/")
        assert "hello get" in body
        body = http_post("127.0.0.1", port, "/", data="foo=bar")
        assert "hello post" in body
        httpd.shutdown()
        t.join()
    print("[SUCCESS] HTTP GET/POST test")

def test_http_server():
    import threading
    import time
    import os
    from kn_sock import start_http_server, http_get, http_post
    os.makedirs("test_static", exist_ok=True)
    with open("test_static/index.html", "w") as f:
        f.write("<h1>Static Test</h1>")
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
    shutdown_event = threading.Event()
    import socket
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    server_thread = threading.Thread(
        target=start_http_server,
        args=("127.0.0.1", port),
        kwargs={"static_dir": "test_static", "routes": routes, "shutdown_event": shutdown_event},
        daemon=True
    )
    server_thread.start()
    time.sleep(1)
    # Test static file
    body = http_get("127.0.0.1", port, "/")
    assert "Static Test" in body
    # Test GET route
    body = http_get("127.0.0.1", port, "/hello")
    assert "Hello" in body
    # Test POST route
    body = http_post("127.0.0.1", port, "/echo", data="abc123")
    assert "abc123" in body
    shutdown_event.set()
    server_thread.join()
    print("[SUCCESS] HTTP server static, GET, POST test")

def test_pubsub():
    import threading
    import time
    from kn_sock import start_pubsub_server, PubSubClient
    shutdown_event = threading.Event()
    import socket
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    server_thread = threading.Thread(
        target=start_pubsub_server,
        args=(port,),
        kwargs={"shutdown_event": shutdown_event},
        daemon=True
    )
    server_thread.start()
    time.sleep(1)
    client1 = PubSubClient("127.0.0.1", port)
    client2 = PubSubClient("127.0.0.1", port)
    client1.subscribe("test")
    client2.subscribe("test")
    time.sleep(0.2)
    client1.publish("test", "hello pubsub")
    msg1 = client1.recv(timeout=2)
    msg2 = client2.recv(timeout=2)
    client1.close()
    client2.close()
    shutdown_event.set()
    server_thread.join()
    assert msg1["message"] == "hello pubsub"
    assert msg2["message"] == "hello pubsub"
    print("[SUCCESS] PubSub subscribe/publish test")

def test_rpc():
    import threading
    import time
    from kn_sock import start_rpc_server, RPCClient
    def add(a, b):
        return a + b
    def echo(msg):
        return msg
    funcs = {"add": add, "echo": echo}
    shutdown_event = threading.Event()
    import socket
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    server_thread = threading.Thread(
        target=start_rpc_server,
        args=(port, funcs),
        kwargs={"shutdown_event": shutdown_event},
        daemon=True
    )
    server_thread.start()
    time.sleep(1)
    client = RPCClient("127.0.0.1", port)
    assert client.call("add", 2, 3) == 5
    assert client.call("echo", msg="hi") == "hi"
    try:
        client.call("notfound")
        assert False, "Expected exception for unknown method"
    except Exception as e:
        assert "not found" in str(e)
    client.close()
    shutdown_event.set()
    server_thread.join()
    print("[SUCCESS] RPC server/client test")
