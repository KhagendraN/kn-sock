# TCP Protocol

TCP (Transmission Control Protocol) provides reliable, ordered, and error-checked delivery of data between applications. kn-sock makes TCP communication simple and efficient.

## Overview

TCP is connection-oriented, meaning:
- A connection must be established before data can be sent
- Data is delivered in the same order it was sent
- Lost packets are automatically retransmitted
- Connections are explicitly closed

## Synchronous TCP

### Basic TCP Server

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

### Basic TCP Client

```python
from kn_sock import send_tcp_message

send_tcp_message("localhost", 8080, "Hello, World!")
```

### Threaded TCP Server

For handling multiple clients concurrently:

```python
from kn_sock import start_threaded_tcp_server

def handle_tcp_message(data, addr, client_socket):
    print(f"Received from {addr}: {data.decode('utf-8')}")
    client_socket.sendall(b"Message received")

start_threaded_tcp_server(8080, handle_tcp_message)
```

### Sending Raw Bytes

```python
from kn_sock import send_tcp_bytes

# Send raw bytes instead of strings
data = b'\x01\x02\x03\x04'
send_tcp_bytes("localhost", 8080, data)
```

## Asynchronous TCP

### Async TCP Server

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

### Async TCP Client

```python
import asyncio
from kn_sock import send_tcp_message_async

asyncio.run(send_tcp_message_async("localhost", 8080, "Hello, World!"))
```

## Graceful Shutdown

All TCP server functions support graceful shutdown using shutdown events:

```python
import threading
from kn_sock import start_tcp_server

shutdown_event = threading.Event()

def handler(data, addr, client_socket):
    # Check if shutdown was requested
    if shutdown_event.is_set():
        return
    # Process message...
    pass

# Start server
server_thread = threading.Thread(
    target=start_tcp_server,
    args=(8080, handler),
    kwargs={"shutdown_event": shutdown_event},
    daemon=True
)
server_thread.start()

# Later, to shutdown gracefully:
shutdown_event.set()
```
## Related Topics

- **[TCP Protocol](tcp.md)** - For reliable JSON communication
- **[UDP Protocol](udp.md)** - For fast JSON messaging
- **[File Transfer](file-transfer.md)** - For large data transfer
- **[API Reference](../api-reference.md)** - Complete function documentation 
 