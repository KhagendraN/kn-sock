# UDP Protocol

UDP (User Datagram Protocol) provides connectionless, unreliable communication between applications. kn-sock makes UDP messaging simple and efficient.

## Overview

UDP is connectionless, meaning:
- No connection establishment required
- No guarantee of delivery order
- No automatic retransmission of lost packets
- Lower overhead than TCP
- Ideal for real-time applications

## Synchronous UDP

### Basic UDP Server

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

### Basic UDP Client

```python
from kn_sock import send_udp_message

send_udp_message("localhost", 8080, "Hello, World!")
```

### UDP Server with Response

```python
from kn_sock import start_udp_server

def handle_udp_message(data, addr, server_socket):
    message = data.decode('utf-8')
    print(f"Received from {addr}: {message}")
    
    # Send a response back to the client
    response = f"Echo: {message}"
    server_socket.sendto(response.encode('utf-8'), addr)

start_udp_server(8080, handle_udp_message)
```

## Asynchronous UDP

### Async UDP Server

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

### Async UDP Client

```python
import asyncio
from kn_sock import send_udp_message_async

asyncio.run(send_udp_message_async("localhost", 8080, "Hello, World!"))
```

## UDP Multicast

UDP multicast allows sending messages to multiple recipients simultaneously.

### Multicast Server

```python
from kn_sock import start_udp_multicast_server

def handle_multicast_message(data, addr, server_socket):
    print(f"Received multicast from {addr}: {data.decode('utf-8')}")

# Listen on multicast group 224.0.0.1
start_udp_multicast_server(
    group="224.0.0.1",
    port=8080,
    handler_func=handle_multicast_message,
    listen_ip="0.0.0.0",  # Optional, defaults to "0.0.0.0"
    shutdown_event=None   # Optional, for graceful shutdown
)
```

### Multicast Client

```python
from kn_sock import send_udp_multicast

# Send to multicast group 224.0.0.1
send_udp_multicast(
    group="224.0.0.1",
    port=8080,
    message="Hello, multicast world!",
    ttl=1  # Optional, defaults to 1
)
```

### Multicast Configuration

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `group` | Multicast group address (e.g., '224.0.0.1') | - | Yes |
| `port` | Port number | - | Yes |
| `message` | Message to send | - | Yes |
| `ttl` | Time To Live for multicast packets | 1 | No |
| `listen_ip` | Local IP to bind to (server) | "0.0.0.0" | No |
| `shutdown_event` | Event for graceful shutdown (server) | None | No |
| `ttl` | Time-to-live for multicast packets | 1 |
| `listen_ip` | IP to listen on for multicast | '0.0.0.0' |

## Related Topics

- **[TCP Protocol](tcp.md)** - For reliable, connection-oriented communication
- **[JSON Communication](json.md)** - For structured data over UDP
- **[API Reference](../api-reference.md)** - Complete function documentation 