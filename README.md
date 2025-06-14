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

### UDP Messaging

#### Synchronous UDP Server

```python
from kn_sock import start_udp_server

def handle_udp_message(data, addr, server_socket):
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
    # Your message handling code here
    pass
```

### `retry`

Retries a function upon failure, with a delay between attempts.

```python
from kn_sock.decorators import retry

@retry(retries=3, delay=1.0, exceptions=(Exception,))
def handle_message(data, addr, client_socket):
    # Your message handling code here
    pass
```

### `measure_time`

Measures and prints the execution time of the wrapped function.

```python
from kn_sock.decorators import measure_time

@measure_time
def handle_message(data, addr, client_socket):
    # Your message handling code here
    pass
```

### `ensure_json_input`

Validates that the first argument is a valid JSON object (dict or str). Raises `InvalidJSONError` otherwise.

```python
from kn_sock.decorators import ensure_json_input

@ensure_json_input
def handle_json_message(data, addr, client_socket):
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

### TCP Functions

- `start_tcp_server(port, handler_func, host='0.0.0.0')`
- `start_threaded_tcp_server(port, handler_func, host='0.0.0.0')`
- `send_tcp_message(host, port, message)`
- `send_tcp_bytes(host, port, data)`
- `start_async_tcp_server(port, handler_func, host='0.0.0.0')`
- `send_tcp_message_async(host, port, message)`

### UDP Functions

- `start_udp_server(port, handler_func, host='0.0.0.0')`
- `send_udp_message(host, port, message)`
- `start_udp_server_async(port, handler_func, host='0.0.0.0')`
- `send_udp_message_async(host, port, message)`

### JSON Functions

- `start_json_server(port, handler_func, host='0.0.0.0')`
- `send_json(host, port, data)`

### File Transfer Functions

- `send_file(host, port, filepath)`
- `start_file_server(port, save_dir, host='0.0.0.0')`
- `send_file_async(host, port, filepath)`
- `start_file_server_async(port, save_dir, host='0.0.0.0')`

### Decorators

- `log_exceptions(raise_error=True)`
- `retry(retries=3, delay=1.0, exceptions=(Exception,))`
- `measure_time(func)`
- `ensure_json_input(func)`

### Utilities

- `get_free_port()`
- `get_local_ip()`
- `chunked_file_reader(filepath, chunk_size=4096)`
- `recv_all(sock, total_bytes)`
- `print_progress(received_bytes, total_bytes)`
- `is_valid_json(json_string)`

## Contributing

Contributions are welcome! Please read the contributing guidelines first.

## License

[![License](https://img.shields.io/pypi/l/kn-sock)](https://github.com/KhagendraN/kn-sock/blob/main/LICENSE)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
