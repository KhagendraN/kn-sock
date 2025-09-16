# Getting Started

Welcome to kn-sock! This guide will help you get up and running with the library quickly.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install kn-sock

```bash
pip install kn-sock
```

### Optional Dependencies

For advanced features like video chat and live streaming, you may need additional packages:

```bash
# For video/audio features
pip install opencv-python pyaudio numpy

# For compression support
pip install tqdm

# For protocol buffers
pip install protobuf
```

## Basic Concepts

kn-sock is built around a few core concepts:

### 1. Server-Client Pattern

Most kn-sock functionality follows a server-client pattern:

- **Server**: Listens for incoming connections and handles requests
- **Client**: Connects to servers and sends requests

### 2. Message Handlers

Servers use message handler functions to process incoming data:

```python
def handle_message(data, addr, client_socket):
    # Process the received data
    print(f"Received: {data.decode()}")
    # Send a response
    client_socket.sendall(b"Response")
```

### 3. Synchronous vs Asynchronous

kn-sock supports both synchronous and asynchronous operations:

- **Synchronous**: Blocking operations, simpler to understand
- **Asynchronous**: Non-blocking operations, better for high-performance applications

## Your First kn-sock Application

Let's create a simple echo server and client:

### Step 1: Create the Server

Create a file called `server.py`:

```python
from kn_sock import start_tcp_server

def echo_handler(data, addr, client_socket):
    """Echo back any message received"""
    message = data.decode('utf-8')
    print(f"Received from {addr}: {message}")
    
    # Echo the message back
    response = f"Echo: {message}"
    client_socket.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    print("Starting echo server on port 8080...")
    start_tcp_server(8080, echo_handler)
```

### Step 2: Create the Client

Create a file called `client.py`:

```python
from kn_sock import send_tcp_message

if __name__ == "__main__":
    message = "Hello, kn-sock!"
    print(f"Sending: {message}")
    
    send_tcp_message("localhost", 8080, message)
    print("Message sent!")
```

### Step 3: Run the Application

1. Start the server in one terminal:
   ```bash
   python server.py
   ```

2. Run the client in another terminal:
   ```bash
   python client.py
   ```

You should see the message being sent and echoed back!

## Next Steps

Now that you have the basics, explore these areas:

- **[TCP Protocol](protocols/tcp.md)** - Learn about TCP communication
- **[UDP Protocol](protocols/udp.md)** - Discover UDP messaging
- **[JSON Communication](protocols/json.md)** - Send structured data
- **[File Transfer](protocols/file-transfer.md)** - Transfer files between systems

## Common Patterns

### Graceful Shutdown

For production applications, use shutdown events:

```python
import threading
from kn_sock import start_tcp_server

shutdown_event = threading.Event()

def handler(data, addr, client_socket):
    # Your handler code here
    pass

# Start server with shutdown event
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

### Error Handling

Always handle potential errors:

```python
from kn_sock.errors import EasySocketError, ConnectionTimeoutError

try:
    send_tcp_message("localhost", 8080, "Hello")
except ConnectionTimeoutError:
    print("Connection timed out")
except EasySocketError as e:
    print(f"Socket error: {e}")
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Use a different port number
2. **Connection refused**: Make sure the server is running
3. **Permission denied**: Check if you have permission to bind to the port

### Getting Help

- Check the [API Reference](api-reference.md) for detailed function documentation
- Look at the [examples](../examples/) for working code samples
- Visit the [GitHub repository](https://github.com/KhagendraN/kn-sock) for issues and discussions 