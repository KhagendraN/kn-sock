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
start_udp_multicast_server("224.0.0.1", 8080, handle_multicast_message)
```

### Multicast Client

```python
from kn_sock import send_udp_multicast

# Send to multicast group 224.0.0.1
send_udp_multicast("224.0.0.1", 8080, "Hello, multicast world!")
```

### Multicast Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `group` | Multicast group address | Required |
| `port` | Port number | Required |
| `ttl` | Time-to-live for multicast packets | 1 |
| `listen_ip` | IP to listen on for multicast | '0.0.0.0' |

## Use Cases

### Real-time Data Broadcasting

```python
from kn_sock import start_udp_server
import time

def broadcast_sensor_data(data, addr, server_socket):
    # Broadcast sensor data to all clients
    timestamp = time.time()
    message = f"Sensor: {data}, Time: {timestamp}"
    print(f"Broadcasting: {message}")

start_udp_server(8080, broadcast_sensor_data)
```

### Gaming/Real-time Applications

```python
from kn_sock import start_udp_server

def handle_game_update(data, addr, server_socket):
    # Handle real-time game updates
    game_state = data.decode('utf-8')
    print(f"Game update from {addr}: {game_state}")
    
    # Broadcast to other players
    # (Implementation depends on your game logic)

start_udp_server(8080, handle_game_update)
```

### IoT Device Communication

```python
from kn_sock import start_udp_server
import json

def handle_iot_message(data, addr, server_socket):
    try:
        message = json.loads(data.decode('utf-8'))
        device_id = message.get('device_id')
        sensor_value = message.get('value')
        
        print(f"Device {device_id}: {sensor_value}")
        
        # Send acknowledgment
        ack = json.dumps({"status": "received", "device_id": device_id})
        server_socket.sendto(ack.encode('utf-8'), addr)
        
    except json.JSONDecodeError:
        print(f"Invalid JSON from {addr}")

start_udp_server(8080, handle_iot_message)
```

## Error Handling

```python
from kn_sock.errors import EasySocketError, ConnectionTimeoutError

try:
    start_udp_server(8080, handler)
except EasySocketError as e:
    print(f"UDP server error: {e}")

try:
    send_udp_message("localhost", 8080, "Hello")
except EasySocketError as e:
    print(f"UDP client error: {e}")
```

## Performance Considerations

### Message Size

UDP has a maximum message size limit. For large data:

```python
def send_large_data(host, port, data):
    # Split large data into chunks
    chunk_size = 1024
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    for i, chunk in enumerate(chunks):
        message = f"CHUNK:{i}:{len(chunks)}:{chunk.hex()}"
        send_udp_message(host, port, message)
```

### Reliability

For applications requiring reliability, implement your own acknowledgment system:

```python
def reliable_udp_send(host, port, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            send_udp_message(host, port, message)
            # Wait for acknowledgment
            # (Implementation depends on your protocol)
            return True
        except EasySocketError:
            if attempt == max_retries - 1:
                raise
            time.sleep(0.1 * (attempt + 1))  # Exponential backoff
```

## Graceful Shutdown

```python
import threading
from kn_sock import start_udp_server

shutdown_event = threading.Event()

def handler(data, addr, server_socket):
    if shutdown_event.is_set():
        return
    # Process message...
    pass

server_thread = threading.Thread(
    target=start_udp_server,
    args=(8080, handler),
    kwargs={"shutdown_event": shutdown_event},
    daemon=True
)
server_thread.start()

# Later, to shutdown gracefully:
shutdown_event.set()
```

## CLI Usage

```bash
# Start a UDP server
kn-sock run-udp-server 8080

# Send a UDP message
kn-sock send-udp localhost 8080 "Hello, World!"

# Send multicast message
kn-sock send-udp-multicast 224.0.0.1 8080 "Hello, multicast!"
```

## Best Practices

1. **Handle packet loss**: UDP doesn't guarantee delivery
2. **Implement timeouts**: Set appropriate timeouts for your use case
3. **Use appropriate message sizes**: Keep messages under MTU size
4. **Consider reliability needs**: Implement acknowledgments if needed
5. **Use multicast wisely**: Only for one-to-many communication
6. **Handle network errors**: Implement proper error handling

## When to Use UDP

### Use UDP for:
- Real-time applications (gaming, streaming)
- Broadcasting/multicasting
- Simple request-response protocols
- Applications where speed is more important than reliability
- IoT device communication

### Use TCP instead for:
- File transfers
- Database connections
- Applications requiring guaranteed delivery
- Complex protocols requiring ordered data

## Related Topics

- **[TCP Protocol](tcp.md)** - For reliable, connection-oriented communication
- **[JSON Communication](json.md)** - For structured data over UDP
- **[API Reference](../api-reference.md)** - Complete function documentation 