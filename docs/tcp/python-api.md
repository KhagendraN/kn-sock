# Using the Python API

The `kn_sock` Python API allows you to build, test, and scale TCP servers and clients directly in your applications. Use it to create synchronous or asynchronous servers, send messages, or manage secure connections.

## API Quickstart

These examples help you get started with the most common use cases.

### Start a Simple TCP Echo Server

```python
from kn_sock import start_tcp_server

def echo_handler(data, addr, conn):
    conn.sendall(b"Echo: " + data)

start_tcp_server(8080, echo_handler)
```

### Send a TCP Message

```python
from kn_sock import send_tcp_message

send_tcp_message('127.0.0.1', 8080, "Hello TCP")
```

### Send Raw Bytes

```python
from kn_sock import send_tcp_bytes

send_tcp_bytes('127.0.0.1', 8080, b"\x00\x01\x02")
```

### Start an Async TCP Server

```python
import asyncio
from kn_sock import start_async_tcp_server

async def echo_handler(reader, writer):
    data = await reader.read(1024)
    writer.write(b"Echo: " + data)
    await writer.drain()
    writer.close()

asyncio.run(start_async_tcp_server(8081, echo_handler))
```

### Send a Secure Message (TLS)

```python
from kn_sock import send_ssl_tcp_message

send_ssl_tcp_message('127.0.0.1', 8443, "Secure Hello")
```

### Example: Server + Client

=== "Server"

```python
from kn_sock import start_tcp_server

def echo_handler(data, addr, conn):
    print(f"Received from {addr}: {data.decode()}")
    conn.sendall(b"Echo: " + data)

start_tcp_server(8080, echo_handler)
```

=== "Client"

```python
from kn_sock import send_tcp_message

send_tcp_message('127.0.0.1', 8080, "Hello TCP")
```

#### Sample Output

**Server Terminal:**

```
[TCP] Server listening on 0.0.0.0:8080
[TCP][SERVER] Received from ('172.18.0.1', 49906): b'Hello TCP'
```

**Client Terminal:**

```
[TCP] Server response: Echo: Hello TCP
```

### Async Client Example

```python
import asyncio
from kn_sock import send_tcp_message_async

async def main():
    await send_tcp_message_async('127.0.0.1', 8080, "Async Hello")

asyncio.run(main())
```

### When to Use Sync vs Async

| Scenario                        | Use                              |
|---------------------------------|----------------------------------|
| Simple, single-threaded scripts | Synchronous API                  |
| Handling many simultaneous connections | Asynchronous API with asyncio    |
| Performance under high I/O load | Async server + client            |
| Secure, encrypted messaging     | SSL/TLS server and client functions |

## Related Topics

- [Full Reference Documentation](reference.md)
- [Run Manual Tests](testing.md)
- [Use the CLI for quick testing](cli.md)