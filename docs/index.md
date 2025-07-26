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

start_file_server(8080, "/path/to/save/directory")
```

#### File Client

```python
from kn_sock import send_file

send_file("localhost", 8080, "path/to/your/file.txt")
```

#### Async File Transfer

```python
from kn_sock import start_file_server_async, send_file_async
import asyncio

# Async server
asyncio.run(start_file_server_async(8080, "/path/to/save/directory"))

# Async client
asyncio.run(send_file_async("localhost", 8080, "path/to/your/file.txt"))
```

### File Transfer Progress Bars

All file transfer functions in kn_sock support progress bars using tqdm. By default, a progress bar is shown if tqdm is installed.

- To disable, pass `show_progress=False` to any file transfer function.
- Progress bars show bytes transferred, speed, and ETA.

Example:

```python
from kn_sock import send_file
send_file('localhost', 8080, 'file.txt', show_progress=True)
```

## Live Video/Audio Streaming (Multi-Video Selection)

The `kn_sock` library supports live video and audio streaming from one or more video files to multiple clients, with adaptive bitrate and smooth playback.

> **Note:** For best compatibility, use video files encoded as mp4 (H.264). Some formats (e.g., AV1) may not be supported by your OpenCV/FFmpeg installation.

### Features

- **Multi-Video Support**: Server can offer multiple videos; clients select which to play
- **Adaptive Bitrate**: Server adjusts video quality per client based on buffer feedback
- **Jitter Buffer**: Client-side buffering for smooth video/audio playback
- **Robust Audio Protocol**: Audio stream uses magic numbers and timestamps for resynchronization
- **Real-time Feedback**: Client sends buffer status to server for quality adjustment

### Live Stream Server (Python)

```python
from kn_sock import start_live_stream

# Start a live stream server with multiple videos
start_live_stream(9000, ["video1.mp4", "video2.mp4", "video3.mp4"])

# Or with a single video
start_live_stream(9000, ["video.mp4"])
```

### Live Stream Client (Python)

```python
from kn_sock import connect_to_live_server

# Connect to a live stream server
connect_to_live_server("192.168.1.10", 9000)
```

### Advanced Usage with LiveStreamServer/LiveStreamClient

```python
from kn_sock.live_stream import LiveStreamServer, LiveStreamClient

# Server with custom configuration
server = LiveStreamServer(
    video_paths=["video1.mp4", "video2.mp4"],
    host='0.0.0.0',
    video_port=8000,
    audio_port=8001,
    control_port=8010
)
server.start()

# Client with custom buffer settings
client = LiveStreamClient(
    host='127.0.0.1',
    video_port=8000,
    audio_port=8001,
    control_port=8010,
    video_buffer_ms=200,  # 200ms video buffer
    audio_buffer_ms=100,  # 100ms audio buffer
    video_fps=30
)
client.start()
```

### Live Streaming via CLI

- **Start a live stream server with multiple videos:**

```bash
kn-sock run-live-server 9000 video1.mp4 video2.mp4 video3.mp4
# Optional: --host 0.0.0.0 --audio-port 9001
```

- **Connect as a live stream client:**

```bash
kn-sock connect-live-server 192.168.1.10 9000
# Optional: --audio-port 9001
```

### How It Works

1. **Server Setup**: Server extracts audio from video files using FFmpeg
2. **Client Connection**: Client connects to video, audio, and control ports
3. **Video Selection**: If multiple videos are available, client is prompted to select one
4. **Streaming**: Server streams video frames and audio chunks with timestamps
5. **Adaptive Quality**: Client sends buffer feedback; server adjusts JPEG quality (40-90)
6. **Smooth Playback**: Client uses jitter buffers to smooth out network irregularities

### Protocol Details

- **Video Protocol**: Each frame is sent as `[8-byte timestamp][4-byte length][JPEG data]`
- **Audio Protocol**: Each chunk is sent as `[4-byte magic][8-byte timestamp][4-byte length][audio data]`
- **Control Protocol**: Client sends JSON feedback: `{"buffer_level": 0.2}`

### Requirements

- **Python Dependencies**: `opencv-python`, `pyaudio`, `numpy`
- **System Dependencies**: `ffmpeg` (for audio extraction)
- **Network**: TCP ports for video, audio, and control streams

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

## Async WebSocket Client

kn_sock provides an asyncio-compatible WebSocket client for modern, non-blocking applications.

### Usage Example

```python
import asyncio
from kn_sock.websocket import async_connect_websocket

async def main():
    ws = await async_connect_websocket('localhost', 8765)
    await ws.send('Hello async WebSocket!')
    reply = await ws.recv()
    print(f"Received: {reply}")
    await ws.close()

asyncio.run(main())
```

- `async_connect_websocket(host, port, resource='/', headers=None) -> AsyncWebSocketConnection`: Connects asynchronously to a WebSocket server.
- `AsyncWebSocketConnection.send(message: str)`: Send a text message (async).
- `AsyncWebSocketConnection.recv() -> str`: Receive a text message (async).
- `AsyncWebSocketConnection.close()`: Close the connection (async).

This enables fully async WebSocket clients for chat, dashboards, and real-time apps.

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
- `send_udp_multicast(group, port, message, ttl=1)`
- `start_udp_multicast_server(group, port, handler_func, listen_ip='0.0.0.0', shutdown_event=None)`

### File Transfer Functions

- `send_file(host, port, filepath)`
- `start_file_server(port, save_dir, host='0.0.0.0')`
- `send_file_async(host, port, filepath)`
- `start_file_server_async(port, save_dir, host='0.0.0.0')`

### JSON Functions

- `start_json_server(port, handler_func, host='0.0.0.0')`
- `send_json(host, port, obj, timeout=5)`
- `start_json_server_async(port, handler_func, host='0.0.0.0')`
- `send_json_async(host, port, obj)`
- `send_json_response(sock, data)`
- `send_json_response_async(writer, data)`

### WebSocket Functions

- `start_websocket_server(host, port, handler, shutdown_event=None)`
- `connect_websocket(host, port, resource='/', headers=None)`

### HTTP/HTTPS Functions

- `http_get(host, port=80, path='/', headers=None)`
- `http_post(host, port=80, path='/', data='', headers=None)`
- `https_get(host, port=443, path='/', headers=None, cafile=None)`
- `https_post(host, port=443, path='/', data='', headers=None, cafile=None)`
- `start_http_server(host, port, static_dir=None, routes=None, shutdown_event=None)`

### Pub/Sub Functions

- `start_pubsub_server(port, handler_func=None, host='0.0.0.0', shutdown_event=None)`
- `PubSubClient(host, port)`

### RPC Functions

- `start_rpc_server(port, register_funcs, host='0.0.0.0', shutdown_event=None)`
- `RPCClient(host, port)`

### Live Streaming Functions

- `start_live_stream(port, video_paths, host='0.0.0.0', audio_port=None)`
- `connect_to_live_server(ip, port, audio_port=None)`

## Multi-Client Video Chat with Voice

The `kn_sock` library now supports real-time multi-client video chat with voice, allowing multiple users to join a room and communicate with both video and audio in real time.

### Features
- **Multi-client support**: Multiple users can join the same room and see/hear each other.
- **Rooms/Channels**: Users can join named rooms; only users in the same room see/hear each other.
- **User Nicknames**: Each client can set a nickname, which is shared with the server and other clients.
- **Text Chat**: Real-time text messaging with chat overlay on video window.
- **Mute/Unmute**: Toggle audio on/off with keyboard shortcut.
- **Video On/Off**: Toggle video camera on/off with keyboard shortcut.
- **Real-time video and audio**: Uses OpenCV for video and PyAudio for audio.
- **Simple API**: Easy to start a server or connect as a client.

### Requirements
- **Python Dependencies**: `opencv-python`, `pyaudio`, `numpy`, `pickle`
- **Hardware**: Webcam and microphone for each client
- **Network**: TCP ports for video, audio, and text streams (default: 9000, 9001, and 9002)

> **Note:** Audio functionality requires proper PyAudio setup. If you encounter audio issues, you can disable audio and still use video and text chat features.

### Example: Video Chat Server

```python
from kn_sock.video_chat import VideoChatServer

server = VideoChatServer(host='0.0.0.0', video_port=9000, audio_port=9001, text_port=9002)
server.start()
print('Video chat server started on ports 9000 (video), 9001 (audio), and 9002 (text).')

# Keep the server running
try:
    while True:
        pass
except KeyboardInterrupt:
    print('Server stopped.')
```

### Example: Video Chat Client (with Room and Nickname)

```python
from kn_sock.video_chat import VideoChatClient

client = VideoChatClient(server_ip='127.0.0.1', video_port=9000, audio_port=9001, text_port=9002, room='myroom', nickname='alice')
client.start()
print('Connected to video chat server in room "myroom" as "alice".')

# Keep the client running
try:
    while client.running:
        pass
except KeyboardInterrupt:
    print('Client stopped.')
```

### Client Controls

When the video window is active, you can use these keyboard shortcuts:

- **`m`**: Mute/unmute your microphone
- **`v`**: Toggle your video camera on/off
- **`q`**: Quit the application

### Text Chat

- Type messages in the terminal and press Enter to send
- Chat messages appear as an overlay on the video window
- Messages include timestamps and sender nicknames
- Only users in the same room receive the messages

### CLI Example

You can also use the provided example scripts:

```bash
# Start the server
python examples/video_chat_server.py

# Start a client (in another terminal)
python examples/video_chat_client.py <server_ip> <room> <nickname>
```

### CLI Commands

The `kn-sock` CLI also supports video chat commands:

```bash
# Start a video chat server
kn-sock run-video-chat-server --host 0.0.0.0 --video-port 9000 --audio-port 9001 --text-port 9002

# Connect to a video chat server
kn-sock connect-video-chat <server_ip> <room> <nickname> --video-port 9000 --audio-port 9001 --text-port 9002
```

> **Note:** Press 'q' in the video window or Ctrl+C in the terminal to stop the client.

### Troubleshooting

If you encounter issues with video or audio, run the diagnostic tool first:

```bash
python examples/video_chat_diagnostic.py
```

#### Common Issues and Solutions:

**Audio Issues (Most Common):**
If you encounter PyAudio assertion errors or audio crashes, try these solutions:

1. **Disable audio temporarily:**
   ```bash
   python examples/video_chat_client.py 127.0.0.1 myroom alice --no-audio
   ```

2. **Use the no-audio client:**
   ```bash
   python examples/video_chat_client_no_audio.py 127.0.0.1 myroom alice
   ```

3. **Test audio separately:**
   ```bash
   python examples/test_audio_only.py
   ```

4. **Install audio drivers (Arch Linux):**
   ```bash
   sudo pacman -S pulseaudio pulseaudio-alsa
   ```

5. **Set audio environment variables:**
   ```bash
   export PULSE_SERVER=unix:/tmp/pulse-socket
   export ALSA_PCM_CARD=0
   ```

**Display Issues:**
```bash
# Set display backend for OpenCV
export QT_QPA_PLATFORM=xcb
```

**Camera Issues:**
- Make sure your camera is not in use by another application
- Check camera permissions
- Try different camera device numbers if you have multiple cameras

**Dependencies:**
```bash
# Install required packages
pip install opencv-python pyaudio numpy
```

**Note:** The video chat feature works perfectly without audio. If you have persistent audio issues, you can still use video and text chat functionality.

---

## Troubleshooting Guide

If you encounter issues while using kn-sock, consult this guide for solutions to common problems across all features (TCP/UDP, SSL, file transfer, video chat, etc.).

### Port Conflicts
- **Error:** `OSError: [Errno 98] Address already in use`
- **Cause:** The port is already used by another process.
- **Solution:**
  - Use a different port number.
  - Find and stop the process using the port (e.g., `lsof -i :8080` or `netstat -tuln`).
  - On Linux, you can kill the process: `sudo kill <PID>`.

### SSL Certificate Issues
- **Error:** `ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]`
- **Cause:** Invalid, missing, or self-signed certificates.
- **Solution:**
  - Ensure you provide the correct `certfile`, `keyfile`, and (if needed) `cafile`.
  - For self-signed certs, use the `--no-verify` flag (CLI) or `verify=False` (Python) for testing only.
  - Regenerate certificates if expired or corrupted.
  - Check file permissions.

### Network Problems
- **Error:** `ConnectionRefusedError`, `TimeoutError`, or no response
- **Cause:**
  - Server not running or listening on a different port/host
  - Firewall or NAT blocking the connection
  - Wrong IP address or hostname
- **Solution:**
  - Double-check server address and port.
  - Ensure the server is running and reachable from the client machine.
  - Temporarily disable firewalls or add exceptions for the relevant ports.
  - Use `ping` or `telnet` to test connectivity.

### File Transfer Issues
- **Error:** `FileNotFoundError`, `PermissionError`, or incomplete transfer
- **Cause:**
  - Invalid file path or missing permissions
  - Network interruption
- **Solution:**
  - Verify file paths and directory permissions.
  - Ensure the file exists and is readable (client) or the save directory is writable (server).
  - Retry the transfer if interrupted.

### Video/Audio Chat Issues
- See the dedicated troubleshooting section under 'Multi-Client Video Chat with Voice' above for audio, camera, and display issues.

### Common Error Messages
- **`Invalid host/port`**: Check your input and use valid hostnames/IPs and port numbers (1-65535).
- **`File not found`**: Ensure the file path is correct and accessible.
- **`Directory not found`**: Check the save directory path for file servers.
- **`SSL: CERTIFICATE_VERIFY_FAILED`**: See SSL section above.
- **`Connection refused`**: Server is not running or wrong address/port.
- **`Address already in use`**: Port conflict; use a different port.
- **`Permission denied`**: Run with appropriate permissions or change file/directory access.

### Still Stuck?
- Run with increased verbosity or logging if available.
- Check the [GitHub Issues](https://github.com/KhagendraN/kn-sock/issues) for similar problems.
- Open a new issue with details about your environment, command, and error message.

---

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

## API Reference

Below is a comprehensive reference for all public functions in kn-sock. Each function includes its signature, parameters, return values, and a brief description. Use this section to quickly look up usage details for any part of the library.

---

### TCP Functions

- **start_tcp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)**
  - Start a synchronous TCP server.
  - **Parameters:**
    - `port` (int): Port to bind.
    - `handler_func` (callable): Function called for each client (data, addr, client_socket).
    - `host` (str): Host to bind (default: '0.0.0.0').
    - `shutdown_event` (threading.Event, optional): For graceful shutdown.
  - **Returns:** None

- **send_tcp_message(host, port, message)**
  - Send a string message over TCP.
  - **Parameters:**
    - `host` (str): Target host.
    - `port` (int): Target port.
    - `message` (str): Message to send.
  - **Returns:** None

- **start_async_tcp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)**
  - Start an async TCP server (see Usage section for handler signature).
  - **Parameters:** Same as above, but handler is async.
  - **Returns:** None

- **send_tcp_message_async(host, port, message)**
  - Send a string message over TCP asynchronously.
  - **Parameters:** Same as above.
  - **Returns:** None

- **start_ssl_tcp_server(port, handler_func, certfile, keyfile, cafile=None, require_client_cert=False, host='0.0.0.0', shutdown_event=None)**
  - Start a secure SSL/TLS TCP server.
  - **Parameters:**
    - `certfile` (str): Path to server certificate (PEM).
    - `keyfile` (str): Path to private key (PEM).
    - `cafile` (str, optional): CA cert for client verification.
    - `require_client_cert` (bool): Require client cert (mutual TLS).
    - Others as above.
  - **Returns:** None

- **send_ssl_tcp_message(host, port, message, cafile=None, certfile=None, keyfile=None, verify=True)**
  - Send a message over SSL/TLS TCP.
  - **Parameters:**
    - `cafile`, `certfile`, `keyfile` as above.
    - `verify` (bool): Verify server cert (default: True).
    - Others as above.
  - **Returns:** None

---

### UDP Functions

- **start_udp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)**
  - Start a synchronous UDP server.
  - **Parameters:**
    - `handler_func` (callable): (data, addr, server_socket).
    - Others as above.
  - **Returns:** None

- **send_udp_message(host, port, message)**
  - Send a string message over UDP.
  - **Parameters:** Same as TCP.
  - **Returns:** None

---

### File Transfer Functions

- **send_file(host, port, filepath)**
  - Send a file over TCP.
  - **Parameters:**
    - `filepath` (str): Path to file to send.
    - Others as above.
  - **Returns:** None

- **start_file_server(port, save_dir, host='0.0.0.0')**
  - Start a TCP file receiver.
  - **Parameters:**
    - `save_dir` (str): Directory to save received files.
    - Others as above.
  - **Returns:** None

---

### JSON Socket Functions

- **start_json_server(port, handler_func, host='0.0.0.0')**
  - Start a JSON-over-TCP server.
  - **Parameters:**
    - `handler_func` (callable): (data: dict, addr, client_socket).
    - Others as above.
  - **Returns:** None

- **send_json(host, port, obj, timeout=5)**
  - Send a JSON object over TCP.
  - **Parameters:**
    - `obj` (dict): JSON-serializable object.
    - `timeout` (int): Timeout in seconds.
    - Others as above.
  - **Returns:** None

---

### WebSocket Functions

- **start_websocket_server(host, port, handler, shutdown_event=None)**
  - Start a WebSocket server.
  - **Parameters:**
    - `handler` (callable): (ws) handler for each client.
    - Others as above.
  - **Returns:** None

- **connect_websocket(host, port, resource='/', headers=None)**
  - Connect to a WebSocket server.
  - **Parameters:**
    - `resource` (str): WebSocket resource path.
    - `headers` (dict, optional): Extra headers.
    - Others as above.
  - **Returns:** WebSocket client object

---

### HTTP/HTTPS Functions

- **http_get(host, port=80, path='/', headers=None)**
- **http_post(host, port=80, path='/', data='', headers=None)**
- **https_get(host, port=443, path='/', headers=None, cafile=None)**
- **https_post(host, port=443, path='/', data='', headers=None, cafile=None)**
  - Simple HTTP/HTTPS client helpers.
  - **Parameters:**
    - `path` (str): URL path.
    - `data` (str): POST data.
    - `headers` (dict): HTTP headers.
    - `cafile` (str): CA cert for HTTPS.
    - Others as above.
  - **Returns:** Response body (str)

---

### Pub/Sub Functions

- **start_pubsub_server(port, handler_func=None, host='0.0.0.0', shutdown_event=None)**
  - Start a pub/sub server.
  - **Parameters:**
    - `handler_func` (callable, optional): Custom handler.
    - Others as above.
  - **Returns:** None

- **PubSubClient(host, port)**
  - Pub/sub client class.
  - **Methods:**
    - `subscribe(topic)`
    - `unsubscribe(topic)`
    - `publish(topic, message)`
    - `recv(timeout=None)`
  - **Returns:** None or message (str)

---

### RPC Functions

- **start_rpc_server(port, register_funcs, host='0.0.0.0', shutdown_event=None)**
  - Start an RPC server.
  - **Parameters:**
    - `register_funcs` (dict): Function name to callable.
    - Others as above.
  - **Returns:** None

- **RPCClient(host, port)**
  - RPC client class.
  - **Methods:**
    - `call(function, *args, **kwargs)`
  - **Returns:** Result of remote function

---

### Live Streaming Functions

- **start_live_stream(port, video_paths, host='0.0.0.0', audio_port=None)**
  - Start a live video/audio stream server.
  - **Parameters:**
    - `video_paths` (list of str): Video file paths.
    - `audio_port` (int, optional): Audio port.
    - Others as above.
  - **Returns:** None

- **connect_to_live_server(ip, port, audio_port=None)**
  - Connect to a live stream server.
  - **Parameters:**
    - `ip` (str): Server IP.
    - `port` (int): Video port.
    - `audio_port` (int, optional): Audio port.
  - **Returns:** None

---

### Video Chat Functions

- **VideoChatServer(host='0.0.0.0', video_port=9000, audio_port=9001, text_port=9002)**
  - Multi-client video chat server class.
  - **Methods:**
    - `start()`
  - **Parameters:**
    - `host` (str): Host to bind.
    - `video_port`, `audio_port`, `text_port` (int): Ports for each stream.
  - **Returns:** None

- **VideoChatClient(server_ip, video_port=9000, audio_port=9001, text_port=9002, room='default', nickname='user')**
  - Video chat client class.
  - **Methods:**
    - `start()`
  - **Parameters:**
    - `server_ip` (str): Server IP.
    - `room` (str): Room name.
    - `nickname` (str): User nickname.
    - Ports as above.
  - **Returns:** None

---

### Utilities

- **get_free_port()**
  - Find a free TCP port.
  - **Returns:** int

- **get_local_ip()**
  - Get the local IP address.
  - **Returns:** str

- **chunked_file_reader(filepath, chunk_size=4096)**
  - Yield file data in chunks.
  - **Parameters:**
    - `filepath` (str): Path to file.
    - `chunk_size` (int): Bytes per chunk.
  - **Returns:** Iterator[bytes]

- **recv_all(sock, total_bytes)**
  - Receive exactly `total_bytes` from a socket.
  - **Parameters:**
    - `sock` (socket.socket): Socket.
    - `total_bytes` (int): Number of bytes to receive.
  - **Returns:** bytes

- **print_progress(received_bytes, total_bytes)**
  - Print file transfer progress.
  - **Parameters:**
    - `received_bytes` (int)
    - `total_bytes` (int)
  - **Returns:** None

- **is_valid_json(json_string)**
  - Check if a string is valid JSON.
  - **Parameters:**
    - `json_string` (str)
  - **Returns:** bool

---

### Errors

- **EasySocketError**: Base exception for all kn_sock errors.
- **ConnectionTimeoutError**: Raised on connection or read/write timeout.
- **PortInUseError**: Raised when a port is already in use.
- **InvalidJSONError**: Raised when a JSON message cannot be decoded.
- **UnsupportedProtocolError**: Raised for unsupported protocols.
- **FileTransferError**: Raised when file transfer fails.

See the 'Errors' section above for usage examples.

---

## Message Compression

kn_sock supports gzip and deflate compression for large messages. Use the compression utilities to reduce network usage for big data transfers.

### Usage

```python
from kn_sock.compression import compress_data, decompress_data, detect_compression

# Compress data
original = b"some large data..."
compressed = compress_data(original, method='gzip')

# Send compressed over socket...

# On the receiving end
detected = detect_compression(compressed)
restored = decompress_data(compressed)
assert restored == original
```

- `compress_data(data: bytes, method: str = 'gzip') -> bytes`: Compress data using gzip or deflate.
- `decompress_data(data: bytes) -> bytes`: Decompress data (auto-detects gzip/deflate).
- `detect_compression(data: bytes) -> str`: Detect compression type ('gzip', 'deflate', or 'none').

Use compression for large file transfers, JSON payloads, or any scenario where bandwidth matters.

## Message Queues

kn_sock provides both in-memory and persistent file-based message queues for reliable, thread-safe message delivery.

### InMemoryQueue

A thread-safe FIFO queue for fast, in-memory message passing.

```python
from kn_sock.queue import InMemoryQueue
q = InMemoryQueue()
q.put('hello')
msg = q.get()
q.task_done()
q.join()
```

### FileQueue

A persistent queue that stores messages on disk, surviving process restarts.

```python
from kn_sock.queue import FileQueue
fq = FileQueue('queue.db')
fq.put('hello')
msg = fq.get()
fq.task_done()
fq.close()
```

- Both queues support FIFO, blocking get, task_done, join, empty, and qsize.
- FileQueue provides at-least-once delivery and is safe for multi-process use (with care).
- Use for background jobs, reliable delivery, or as a building block for pub/sub and task systems.

## Protocol Buffers (Protobuf)

kn_sock supports efficient, type-safe serialization using protocol buffers (protobuf).

### Usage

First, define your .proto file and generate Python classes using protoc:

```bash
protoc --python_out=. my_proto.proto
```

Then use the kn_sock utilities:

```python
from kn_sock.protobuf import serialize_message, deserialize_message
from my_proto_pb2 import MyMessage

msg = MyMessage(field1='abc', field2=123)
data = serialize_message(msg)
restored = deserialize_message(data, MyMessage)
assert restored.field1 == 'abc'
```

- `serialize_message(msg) -> bytes`: Serialize a protobuf message to bytes.
- `deserialize_message(data: bytes, schema) -> object`: Deserialize bytes to a protobuf message (given the schema class).

**Requires:** `pip install protobuf`

Use protobuf for high-performance, cross-language, and type-safe message exchange.

## Load Balancing

kn_sock provides simple load balancing utilities for distributing requests across multiple servers.

### RoundRobinLoadBalancer

Cycles through servers in order, distributing requests evenly.

```python
from kn_sock.load_balancer import RoundRobinLoadBalancer
lb = RoundRobinLoadBalancer()
lb.add_server('127.0.0.1:9000')
lb.add_server('127.0.0.1:9001')
server = lb.get_server()  # Returns next server in round-robin order
```

### LeastConnectionsLoadBalancer

Selects the server with the fewest active connections.

```python
from kn_sock.load_balancer import LeastConnectionsLoadBalancer
lcb = LeastConnectionsLoadBalancer()
lcb.add_server('127.0.0.1:9000')
lcb.update_connections('127.0.0.1:9000', 2)
server = lcb.get_server()  # Returns server with fewest connections
```

- Both support add_server, remove_server, get_server.
- LeastConnectionsLoadBalancer supports update_connections(server, count).
- Use for distributing load in high-availability or scalable systems.

## Interactive CLI

The kn-sock package provides an interactive command-line interface (REPL) for managing TCP connections and sending/receiving messages in real time.

### Starting the CLI

```
python -m kn_sock.cli interactive
```

### Commands

- `connect <name> <host> <port>`: Connect to a server and store the connection by name.
- `list`: List all active connections.
- `select <name>`: Set the default connection for send/receive.
- `send <message>`: Send a message to the default connection.
- `receive`: Receive a message from the default connection.
- `bg_receive`: Toggle background receive mode (prints incoming messages as they arrive).
- `history`: Show last 10 sent/received messages.
- `disconnect <name>`: Disconnect a connection.
- `quit`/`exit`: Exit the CLI.
- `help`: Show help for all commands.

### Example Session

```
connect myconn 127.0.0.1 9000
send Hello, server!
receive
bg_receive
history
list
quit
```

### Tips & Troubleshooting

- If you see 'connection refused', ensure the server is running and reachable.
- If you see encoding errors, check that the server and client use compatible text encodings (UTF-8 is default).
- Use `bg_receive` to monitor incoming messages in real time.
- Use `history` to review recent sent/received messages.
