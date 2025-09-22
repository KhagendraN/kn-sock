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

## Secure TCP (SSL/TLS)

kn-sock supports secure TCP communication using SSL/TLS for encrypted connections.

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

### SSL/TLS Configuration

| Parameter | Description | Required |
|-----------|-------------|----------|
| `certfile` | Path to server certificate (PEM) | Yes |
| `keyfile` | Path to private key (PEM) | Yes |
| `cafile` | CA certificate for verification | No |
| `require_client_cert` | Require client certificate (mutual TLS) | No |
| `verify` | Verify server certificate (client) | Yes (default: True) |

### Generating SSL Certificates

For testing, generate self-signed certificates:

```bash
# Generate private key
openssl genrsa -out server.key 2048

# Generate certificate
openssl req -new -x509 -key server.key -out server.crt -days 365

# For client certificates (mutual TLS)
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr
openssl x509 -req -in client.csr -CA server.crt -CAkey server.key -out client.crt
```

## TCP Connection Pooling

For high-performance applications that make frequent connections, use connection pooling:

### Basic Connection Pool

```python
from kn_sock import TCPConnectionPool

pool = TCPConnectionPool('localhost', 8080, max_size=5, idle_timeout=30)
with pool.connection() as conn:
    conn.sendall(b"Hello")
    data = conn.recv(1024)
    print(data)

pool.closeall()  # Clean up all connections
```

### Secure Connection Pool

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

### Pool Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `max_size` | Maximum number of pooled connections | 10 |
| `idle_timeout` | Seconds before idle connections are closed | 60 |
| `ssl` | Enable SSL/TLS | False |
| `cafile` | CA certificate for verification | None |
| `certfile` | Client certificate | None |
| `keyfile` | Client private key | None |
| `verify` | Verify server certificate | True |

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

## Error Handling

```python
from kn_sock.errors import EasySocketError, ConnectionTimeoutError, PortInUseError

try:
    start_tcp_server(8080, handler)
except PortInUseError:
    print("Port 8080 is already in use")
except EasySocketError as e:
    print(f"Socket error: {e}")

try:
    send_tcp_message("localhost", 8080, "Hello")
except ConnectionTimeoutError:
    print("Connection timed out")
except EasySocketError as e:
    print(f"Client error: {e}")
```

## Performance Tips

1. **Use connection pooling** for frequent connections
2. **Use async servers** for high-concurrency applications
3. **Implement proper error handling** for production use
4. **Use SSL/TLS** for sensitive data transmission
5. **Set appropriate timeouts** for your use case

## CLI Usage

```bash
# Start a TCP server
kn-sock run-tcp-server 8080

# Send a TCP message
kn-sock send-tcp localhost 8080 "Hello, World!"

# Start a secure TCP server
kn-sock run-ssl-tcp-server 8443 server.crt server.key

# Send a secure TCP message
kn-sock send-ssl-tcp localhost 8443 "Hello Secure"
```

## Related Topics

- **[UDP Protocol](udp.md)** - For connectionless communication
- **[JSON Communication](json.md)** - For structured data exchange
- **[File Transfer](file-transfer.md)** - For file transmission over TCP
- **[API Reference](../api-reference.md)** - Complete function documentation 