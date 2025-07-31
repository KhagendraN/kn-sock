# Using the Python API

The `kn_sock.udp` module provides a set of synchronous, asynchronous, and multicast utilities for working with UDP sockets. You can use these to send and receive datagrams, build non-blocking event-driven applications, or broadcast messages across a network.

This page offers code examples for quick usage and integration.

## UDP Quickstart

These examples cover the most common use cases.

### Start a UDP Echo Server (Synchronous)

```python
from kn_sock import start_udp_server

def echo_handler(data, addr, sock):
    print(f"Received from {addr}: {data.decode()}")
    sock.sendto(data, addr)

start_udp_server(8081, echo_handler)
```

### Send a UDP Message (Synchronous)

```python
from kn_sock import send_udp_message

send_udp_message("127.0.0.1", 8081, "Hello UDP")
```

#### Expected output:

```
[UDP][SYNC] Sent to 127.0.0.1:8081
```

### Start a UDP Server (Asynchronous)

```python
import asyncio
from kn_sock import start_udp_server_async

async def echo_handler(data, addr, transport):
    print(f"Received from {addr}: {data.decode()}")
    transport.sendto(data, addr)

asyncio.run(start_udp_server_async(8082, echo_handler))
```

### Send a UDP Message (Asynchronous)

```python
import asyncio
from kn_sock import send_udp_message_async

async def main():
    await send_udp_message_async("127.0.0.1", 8082, "Hello from async UDP")

asyncio.run(main())
```

### Multicast Messaging

Use these functions to send and receive multicast packets in a local network.

#### Send a Multicast Message

```python
from kn_sock import send_udp_multicast

send_udp_multicast("224.0.0.1", 9000, "Broadcast message")
```

#### Start a Multicast Server

```python
from kn_sock import start_udp_multicast_server

def handler(data, addr, sock):
    print(f"[MULTICAST] {addr} says: {data.decode()}")

start_udp_multicast_server("224.0.0.1", 9000, handler)
```

#### Note: Multicast reception may require adjusting firewall settings or running in a local network.

### Choosing Between Sync and Async

| Use Case                        | Recommended API                       |
|---------------------------------|---------------------------------------|
| Simple, low-frequency communication | Synchronous (start_udp_server)        |
| Concurrent or event-driven applications | Asynchronous (start_udp_server_async) |
| Fire-and-forget messages         | send_udp_message or send_udp_message_async |
| Broadcast/multicast messaging    | send_udp_multicast, start_udp_multicast_server |

## Related Topics

- [API Reference](reference.md)
- [Testing & Troubleshooting](testing.md)