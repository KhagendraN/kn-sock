<p align="center">
  <img src="kn-sock_logo.png" alt="kn-sock logo" width="128"/>
</p>

# kn-sock

![PyPI version](https://img.shields.io/pypi/v/kn-sock)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/kn-sock)](https://pypi.org/project/kn-sock/)

A simplified socket programming toolkit for Python.

## Features

- **TCP/UDP Messaging**: Supports both synchronous and asynchronous communication.
- **JSON Socket Communication**: Easily send and receive JSON data over sockets.
- **File Transfer over TCP**: Transfer files between clients and servers.
- **Threaded/Multi-Client Support**: Handle multiple clients concurrently.
- **Command-Line Interface**: Simple CLI for quick socket operations.

[![GitHub Stars](https://img.shields.io/github/stars/KhagendraN/kn-sock?style=social)](https://github.com/KhagendraN/kn-sock/stargazers)

## Installation

```bash
pip install kn-sock
```

## Usage

### TCP Messaging

#### Synchronous TCP Server

```python
from kn_sock import start_tcp_server

def handle_tcp_message(data, addr, client_socket):
    """
    Handle incoming TCP messages.

    Args:
        data (bytes): The data received from the client.
        addr (tuple): The address of the client.
        client_socket (socket.socket): The client socket.
    """
    print(f"Received from {addr}: {data.decode('utf-8')}")
    client_socket.sendall(b"Message received")

start_tcp_server(8080, handle_tcp_message)
```

#### Synchronous TCP Client

```python
from kn_sock import send_tcp_message

send_tcp_message("localhost", 8080, "Hello, World!")
```

#### Asynchronous TCP Server

```python
import asyncio
from kn_sock import start_async_tcp_server

async def handle_tcp_message(data, addr, writer):
    """
    Handle incoming TCP messages asynchronously.

    Args:
        data (bytes): The data received from the client.
        addr (tuple): The address of the client.
        writer (asyncio.StreamWriter): The writer object for the client.
    """
    print(f"Received from {addr}: {data.decode('utf-8')}")
    writer.write(b"Message received")
    await writer.drain()

asyncio.run(start_async_tcp_server(8080, handle_tcp_message))
```

#### Asynchronous TCP Client

```python
import asyncio
from kn_sock import send_tcp_message_async

asyncio.run(send_tcp_message_async("localhost", 8080, "Hello, World!"))
```

## Secure TCP (SSL/TLS)

`kn_sock` supports secure TCP communication using SSL/TLS, both in code and via the CLI.

### Synchronous Secure TCP Server

```python
from kn_sock import start_ssl_tcp_server

def handle_secure(data, addr, client_socket):
    print(f"Received from {addr}: {data.decode()}")
    client_socket.sendall(b"Secure response")

start_ssl_tcp_server(
    8443,
    handle_secure,
    certfile="server.crt",
    keyfile="server.key",
    cafile="ca.crt",  # Optional, for client cert verification
    require_client_cert=True  # For mutual TLS
)
```

### Synchronous Secure TCP Client

```python
from kn_sock import send_ssl_tcp_message

send_ssl_tcp_message(
    "localhost", 8443, "Hello Secure",
    cafile="ca.crt",  # Optional, for server verification
    certfile="client.crt", keyfile="client.key"  # For mutual TLS
)
```

### Asynchronous Secure TCP Server

```python
import asyncio
from kn_sock import start_async_ssl_tcp_server

async def handle_secure(data, addr, writer):
    print(f"Received from {addr}: {data.decode()}")
    writer.write(b"Secure response")
    await writer.drain()

asyncio.run(start_async_ssl_tcp_server(
    8443,
    handle_secure,
    certfile="server.crt",
    keyfile="server.key"
))
```

### Asynchronous Secure TCP Client

```python
import asyncio
from kn_sock import send_ssl_tcp_message_async

asyncio.run(send_ssl_tcp_message_async(
    "localhost", 8443, "Hello Secure"
))
```

### CLI Usage

```bash
# Start a secure server
kn-sock run-ssl-tcp-server 8443 server.crt server.key --cafile ca.crt --require-client-cert

# Send a secure message
kn-sock send-ssl-tcp localhost 8443 "Hello Secure" --cafile ca.crt --certfile client.crt --keyfile client.key
```

> **Note:** You must have valid certificate and key files. For testing, you can generate self-signed certificates using OpenSSL.

## TCP Connection Pooling

`kn_sock` provides a TCPConnectionPool for efficient client-side connection reuse. This reduces connection overhead for frequent requests.

### Basic Usage (Plain TCP)

```python
from kn_sock import TCPConnectionPool

pool = TCPConnectionPool('localhost', 8080, max_size=5, idle_timeout=30)
with pool.connection() as conn:
    conn.sendall(b"Hello")
    data = conn.recv(1024)
    print(data)

pool.closeall()  # Clean up all connections
```

### Secure Usage (SSL/TLS)

```python
from kn_sock import TCPConnectionPool

pool = TCPConnectionPool(
    'localhost', 8443, max_size=5, idle_timeout=30,
    ssl=True, cafile="ca.crt", certfile="client.crt", keyfile="client.key", verify=True
)
with pool.connection() as conn:
    conn.sendall(b"Hello Secure")
    data = conn.recv(1024)
    print(data)

pool.closeall()
```

- `max_size`: Maximum number of pooled connections.
- `idle_timeout`: Seconds before idle connections are closed.
- `ssl`, `cafile`, `certfile`, `keyfile`, `verify`: SSL/TLS options.

### UDP Messaging

#### Synchronous UDP Server

```python
from kn_sock import start_udp_server

def handle_udp_message(data, addr, server_socket):
    """
    Handle incoming UDP messages.

    Args:
        data (bytes): The data received from the client.
        addr (tuple): The address of the client.
        server_socket (socket.socket): The server socket.
    """
    print(f"Received from {addr}: {data.decode('utf-8')}")

start_udp_server(8080, handle_udp_message)
```

#### Synchronous UDP Client

```python
from kn_sock import send_udp_message

send_udp_message("localhost", 8080, "Hello, World!")
```

#### Asynchronous UDP Server

```python
import asyncio
from kn_sock import start_udp_server_async

async def handle_udp_message(data, addr, transport):
    """
    Handle incoming UDP messages asynchronously.

    Args:
        data (bytes): The data received from the client.
        addr (tuple): The address of the client.
        transport (asyncio.DatagramTransport): The transport object for the client.
    """
    print(f"Received from {addr}: {data.decode('utf-8')}")

asyncio.run(start_udp_server_async(8080, handle_udp_message))
```

#### Asynchronous UDP Client

```python
import asyncio
from kn_sock import send_udp_message_async

asyncio.run(send_udp_message_async("localhost", 8080, "Hello, World!"))
```

### JSON Socket Communication

#### JSON Server

```python
from kn_sock import start_json_server

def handle_json_message(data, addr, client_socket):
    """
    Handle incoming JSON messages.

    Args:
        data (dict): The JSON data received from the client.
        addr (tuple): The address of the client.
        client_socket (socket.socket): The client socket.
    """
    print(f"Received from {addr}: {data}")
    client_socket.sendall(b'{"status": "received"}')

start_json_server(8080, handle_json_message)
```

#### JSON Client

```python
from kn_sock import send_json

send_json("localhost", 8080, {"message": "Hello, World!"})
```

### File Transfer over TCP

#### File Server

```python
from kn_sock import start_file_server

start_file_server(8080)
```

#### File Client

```python
from kn_sock import send_file

send_file("localhost", 8080, "path/to/your/file.txt")
```

## Live Streaming

The `kn_sock` library supports live video and audio streaming from a video file to multiple clients, using both Python API and CLI.

> **Note:** For best compatibility, use video files encoded as mp4 (H.264). Some formats (e.g., AV1) may not be supported by your OpenCV/FFmpeg installation.

### Live Stream Server (Python)

```python
from kn_sock import start_live_stream

# Start a live stream server on port 9000, streaming from a video file
start_live_stream(9000, "/path/to/video.mp4")
```

### Live Stream Client (Python)

```python
from kn_sock import connect_to_live_server

# Connect to a live stream server at 192.168.1.10:9000
connect_to_live_server("192.168.1.10", 9000)
```

### Live Streaming via CLI

- **Start a live stream server:**

```bash
kn-sock run-live-server 9000 /path/to/video.mp4
# Optional: --host 0.0.0.0 --audio-port 9001
```

- **Connect as a live stream client:**

```bash
kn-sock connect-live-server 192.168.1.10 9000
# Optional: --audio-port 9001
```

## WebSocket Support

kn_sock provides a minimal WebSocket server and client for real-time, bidirectional communication (e.g., chat, dashboards, live updates).

- Use `start_websocket_server(host, port, handler_func, ...)` to start a WebSocket server.
- Use `connect_websocket(host, port, ...)` to connect as a client.

### Example: WebSocket Echo Server

```python
from kn_sock import start_websocket_server
import threading

def echo_handler(ws):
    print(f"[WebSocket][SERVER] Client connected: {ws.addr}")
    try:
        while ws.open:
            msg = ws.recv()
            if not msg:
                break
            ws.send(f"Echo: {msg}")
    finally:
        ws.close()

shutdown_event = threading.Event()
server_thread = threading.Thread(
    target=start_websocket_server,
    args=("127.0.0.1", 8765, echo_handler),
    kwargs={"shutdown_event": shutdown_event},
    daemon=True
)
server_thread.start()
# ... trigger shutdown_event as needed ...
```

### Example: WebSocket Client

```python
from kn_sock import connect_websocket
ws = connect_websocket("127.0.0.1", 8765)
ws.send("Hello WebSocket!")
reply = ws.recv()
print(f"Received: {reply}")
ws.close()
```

> **Note:** This implementation supports text frames only (no binary, no extensions, no SSL for browsers yet). Suitable for Python-to-Python or custom client/server use.

## HTTP/HTTPS Client Support

kn_sock provides simple HTTP and HTTPS client helpers for quick requests without external libraries.

- `http_get(host, port=80, path='/', headers=None)`
- `http_post(host, port=80, path='/', data='', headers=None)`
- `https_get(host, port=443, path='/', headers=None, cafile=None)`
- `https_post(host, port=443, path='/', data='', headers=None, cafile=None)`

### Example: HTTP GET/POST

```python
from kn_sock import http_get, http_post

body = http_get("example.com", 80, "/")
print(body)

body = http_post("httpbin.org", 80, "/post", data="foo=bar&baz=qux")
print(body)
```

### Example: HTTPS GET/POST

```python
from kn_sock import https_get, https_post

body = https_get("example.com", 443, "/")
print(body)

body = https_post("httpbin.org", 443, "/post", data="foo=bar&baz=qux")
print(body)
```

> **Note:** These helpers do not support redirects, chunked encoding, or cookies. For advanced HTTP features, use a full HTTP library.

## HTTP Server

kn_sock provides a minimal HTTP server for serving static files and handling simple API routes.

- Use `start_http_server(host, port, static_dir=None, routes=None, shutdown_event=None)` to start the server.
- `static_dir`: Directory to serve files from (e.g., index.html).
- `routes`: Dict mapping (method, path) to handler functions. Handler signature: (request, client_socket).
- `shutdown_event`: For graceful shutdown.

### Example: Static File and Route Handlers

```python
from kn_sock import start_http_server
import threading
import os

def hello_route(request, client_sock):
    client_sock.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nHello")

def echo_post(request, client_sock):
    body = request['raw'].split(b'\r\n\r\n', 1)[-1]
    resp = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body
    client_sock.sendall(resp)

os.makedirs("static", exist_ok=True)
with open("static/index.html", "w") as f:
    f.write("<h1>Hello from static file!</h1>")
routes = {
    ("GET", "/hello"): hello_route,
    ("POST", "/echo"): echo_post,
}
shutdown_event = threading.Event()
server_thread = threading.Thread(
    target=start_http_server,
    args=("127.0.0.1", 8080),
    kwargs={"static_dir": "static", "routes": routes, "shutdown_event": shutdown_event},
    daemon=True
)
server_thread.start()
# ... trigger shutdown_event as needed ...
```

> **Note:** This server is for prototyping and simple use cases. For production, use a full-featured HTTP server.

## Publish/Subscribe (Pub/Sub)

kn_sock provides a simple TCP-based pub/sub server and client for topic-based messaging.

- Use `start_pubsub_server(port, handler_func=None, host='0.0.0.0', shutdown_event=None)` to start the server.
- Use `PubSubClient(host, port)` for the client. Methods: `subscribe(topic)`, `unsubscribe(topic)`, `publish(topic, message)`, `recv(timeout=None)`.

### Example: Pub/Sub Server

```python
from kn_sock import start_pubsub_server
import threading

shutdown_event = threading.Event()
server_thread = threading.Thread(
    target=start_pubsub_server,
    args=(9000,),
    kwargs={"shutdown_event": shutdown_event},
    daemon=True
)
server_thread.start()
# ... trigger shutdown_event as needed ...
```

### Example: Pub/Sub Client

```python
from kn_sock import PubSubClient
client = PubSubClient("127.0.0.1", 9000)
client.subscribe("news")
client.publish("news", "Hello, subscribers!")
msg = client.recv(timeout=2)
print(msg)
client.close()
```

> **Protocol:** All messages are JSON lines. Actions: `subscribe`, `unsubscribe`, `publish`. Server broadcasts published messages to all subscribers of a topic.

> **Use cases:** Chat rooms, notifications, real-time data updates, event-driven apps.

## Remote Procedure Call (RPC)

kn_sock provides a simple TCP-based JSON-RPC server and client for remote function calls.

- Use `start_rpc_server(port, register_funcs, host='0.0.0.0', shutdown_event=None)` to start the server.
- Use `RPCClient(host, port)` for the client. Method: `call(function, *args, **kwargs)`.

### Example: RPC Server

```python
from kn_sock import start_rpc_server
import threading

def add(a, b):
    return a + b

def echo(msg):
    return msg

funcs = {"add": add, "echo": echo}
shutdown_event = threading.Event()
server_thread = threading.Thread(
    target=start_rpc_server,
    args=(9001, funcs),
    kwargs={"shutdown_event": shutdown_event},
    daemon=True
)
server_thread.start()
# ... trigger shutdown_event as needed ...
```

### Example: RPC Client

```python
from kn_sock import RPCClient
client = RPCClient("127.0.0.1", 9001)
print(client.call("add", 2, 3))
print(client.call("echo", msg="Hello!"))
client.close()
```

> **Protocol:** All requests and responses are JSON lines. Requests: `{method, params, kwargs}`. Responses: `{result}` or `{error}`.

> **Use cases:** Distributed computing, remote control, microservices, automation.

## Command-Line Interface

The `kn-sock` library comes with a simple CLI for quick socket operations. You can use the following commands:

- **Send TCP Message**:

```bash
kn-sock send-tcp localhost 8080 "Hello, World!"
```

- **Start TCP Server**:

```bash
kn-sock run-tcp-server 8080
```

- **Send UDP Message**:

```bash
kn-sock send-udp localhost 8080 "Hello, World!"
```

- **Start UDP Server**:

```bash
kn-sock run-udp-server 8080
```

- **Send File**:

```bash
kn-sock send-file localhost 8080 path/to/your/file.txt
```

- **Start File Server**:

```bash
kn-sock run-file-server 8080 /path/to/save/directory
```

## Decorators

The `.decorators` module provides useful decorators to enhance your socket handlers.

### `log_exceptions`

Logs exceptions and optionally re-raises them.

```python
from kn_sock.decorators import log_exceptions

@log_exceptions(raise_error=True)
def handle_message(data, addr, client_socket):
    """
    Handle incoming messages with exception logging.

    Args:
        data (bytes): The data received from the client.
        addr (tuple): The address of the client.
        client_socket (socket.socket): The client socket.
    """
    # Your message handling code here
    pass
```

### `retry`

Retries a function upon failure, with a delay between attempts.

```python
from kn_sock.decorators import retry

@retry(retries=3, delay=1.0, exceptions=(Exception,))
def handle_message(data, addr, client_socket):
    """
    Handle incoming messages with retry logic.

    Args:
        data (bytes): The data received from the client.
        addr (tuple): The address of the client.
        client_socket (socket.socket): The client socket.
    """
    # Your message handling code here
    pass
```

### `measure_time`

Measures and prints the execution time of the wrapped function.

```python
from kn_sock.decorators import measure_time

@measure_time
def handle_message(data, addr, client_socket):
    """
    Handle incoming messages with execution time measurement.

    Args:
        data (bytes): The data received from the client.
        addr (tuple): The address of the client.
        client_socket (socket.socket): The client socket.
    """
    # Your message handling code here
    pass
```

### `ensure_json_input`

Validates that the first argument is a valid JSON object (dict or str). Raises `InvalidJSONError` otherwise.

```python
from kn_sock.decorators import ensure_json_input

@ensure_json_input
def handle_json_message(data, addr, client_socket):
    """
    Handle incoming JSON messages with input validation.

    Args:
        data (dict): The JSON data received from the client.
        addr (tuple): The address of the client.
        client_socket (socket.socket): The client socket.
    """
    # Your JSON message handling code here
    pass
```

## Utilities

The `.utils` module provides various utility functions to assist with socket programming.

### Network Utilities

#### `get_free_port`

Finds a free port for TCP binding (useful for tests).

```python
from kn_sock.utils import get_free_port

port = get_free_port()
print(f"Free port: {port}")
```

#### `get_local_ip`

Returns the local IP address of the current machine.

```python
from kn_sock.utils import get_local_ip

ip = get_local_ip()
print(f"Local IP: {ip}")
```

### File Utilities

#### `chunked_file_reader`

Yields file data in chunks for streaming transfer.

```python
from kn_sock.utils import chunked_file_reader

for chunk in chunked_file_reader("path/to/your/file.txt"):
    # Process each chunk
    pass
```

#### `recv_all`

Receives exactly `total_bytes` from a socket.

```python
from kn_sock.utils import recv_all

data = recv_all(client_socket, total_bytes)
```

### Progress Display

#### `print_progress`

Prints file transfer progress in percentage.

```python
from kn_sock.utils import print_progress

print_progress(received_bytes, total_bytes)
```

### JSON Utility

#### `is_valid_json`

Checks whether a string is valid JSON.

```python
from kn_sock.utils import is_valid_json

if is_valid_json(json_string):
    print("Valid JSON")
else:
    print("Invalid JSON")
```

## Errors

The `.errors` module defines custom exceptions for the `kn_sock` library.

### `EasySocketError`

Base exception for all `kn_sock` errors.

```python
from kn_sock.errors import EasySocketError

try:
    # Your code here
    pass
except EasySocketError as e:
    print(f"EasySocketError: {e}")
```

### Connection-related Errors

#### `ConnectionTimeoutError`

Raised when a connection or read/write operation times out.

```python
from kn_sock.errors import ConnectionTimeoutError

try:
    # Your code here
    pass
except ConnectionTimeoutError as e:
    print(f"ConnectionTimeoutError: {e}")
```

#### `PortInUseError`

Raised when a specified port is already in use.

```python
from kn_sock.errors import PortInUseError

try:
    # Your code here
    pass
except PortInUseError as e:
    print(f"PortInUseError: {e}")
```

### Data & Protocol Errors

#### `InvalidJSONError`

Raised when a JSON message cannot be decoded.

```python
from kn_sock.errors import InvalidJSONError

try:
    # Your code here
    pass
except InvalidJSONError as e:
    print(f"InvalidJSONError: {e}")
```

#### `UnsupportedProtocolError`

Raised when a requested protocol is not supported.

```python
from kn_sock.errors import UnsupportedProtocolError

try:
    # Your code here
    pass
except UnsupportedProtocolError as e:
    print(f"UnsupportedProtocolError: {e}")
```

### File Transfer Errors

#### `FileTransferError`

Raised when file transfer fails.

```python
from kn_sock.errors import FileTransferError

try:
    # Your code here
    pass
except FileTransferError as e:
    print(f"FileTransferError: {e}")
```

## Available Functions

> **Note:** All server functions (TCP, UDP, SSL, async/sync) accept a `shutdown_event` parameter for graceful shutdown. Use `threading.Event` for sync servers and `asyncio.Event` for async servers.

### TCP Functions

- `start_tcp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)`
- `start_threaded_tcp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)`
- `send_tcp_message(host, port, message)`
- `send_tcp_bytes(host, port, data)`
- `start_async_tcp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)`
- `send_tcp_message_async(host, port, message)`
- `start_ssl_tcp_server(port, handler_func, certfile, keyfile, cafile=None, require_client_cert=False, host='0.0.0.0', shutdown_event=None)`
- `send_ssl_tcp_message(host, port, message, cafile=None, certfile=None, keyfile=None, verify=True)`
- `start_async_ssl_tcp_server(port, handler_func, certfile, keyfile, cafile=None, require_client_cert=False, host='0.0.0.0', shutdown_event=None)`
- `send_ssl_tcp_message_async(host, port, message, cafile=None, certfile=None, keyfile=None, verify=True)`

### UDP Functions

- `start_udp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)`
- `send_udp_message(host, port, message)`
- `start_udp_server_async(port, handler_func, host='0.0.0.0', shutdown_event=None)`
- `send_udp_message_async(host, port, message)`

### JSON Functions

- `start_json_server(port, handler_func, host='0.0.0.0')`
- `send_json(host, port, obj, timeout=5)`
- `start_threaded_json_server(port, handler_func, host='0.0.0.0', shutdown_event=None)`
- `send_json_async(host, port, obj, timeout=5)`

## Real World Examples

Explore ready-to-run scripts that solve common networking problems using kn-sock:

- [IoT Protocol](real_world_examples/iot_protocol.py): Custom JSON protocol for IoT devices
- [File Transfer](real_world_examples/file_transfer.py): Secure file transfer between machines
- [Chat Application](real_world_examples/chat_app.py): Real-time chat using WebSockets
- [Microservice RPC](real_world_examples/microservice_rpc.py): Remote procedure calls between services
- [Remote Control](real_world_examples/remote_control.py): Remote monitoring and control of applications
- [HTTP API Server](real_world_examples/http_api_server.py): Serve static files and simple APIs
- [Live Streaming](real_world_examples/live_streaming.py): Live video/audio streaming
- [Test Utilities](real_world_examples/test_utilities.py): Network test and utility scripts

See the [Real World Examples directory](real_world_examples/) for all scripts and details.