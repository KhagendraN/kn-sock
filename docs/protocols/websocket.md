# WebSocket Protocol

WebSockets provide full-duplex communication over a single TCP connection. kn-sock offers comprehensive WebSocket support for real-time applications.

## Overview

WebSocket features in kn-sock:
- **Full-duplex communication**: Send and receive simultaneously
- **Real-time messaging**: Low-latency bidirectional communication
- **Connection persistence**: Long-lived connections with automatic reconnection
- **Custom protocols**: Support for WebSocket subprotocols
- **Async and sync support**: Both synchronous and asynchronous implementations
- **Built-in ping/pong**: Automatic connection health monitoring

## Basic WebSocket Usage

### WebSocket Server

```python
from kn_sock import start_websocket_server
import threading

def handle_websocket_client(client_socket, address):
    """
    Handle WebSocket client connections.
    
    Args:
        client_socket: The WebSocket client connection
        address: Client address tuple (host, port)
    """
    print(f"WebSocket client connected from {address}")
    
    try:
        while True:
            # Receive message from client
            message = client_socket.recv()
            if message:
                print(f"Received: {message}")
                
                # Echo the message back
                client_socket.send(f"Echo: {message}")
            else:
                # Client disconnected
                break
                
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        print(f"Client {address} disconnected")
        client_socket.close()

# Start WebSocket server
shutdown_event = threading.Event()
start_websocket_server("localhost", 8765, handle_websocket_client, shutdown_event)
```

### WebSocket Client

```python
from kn_sock import connect_websocket
import time

def websocket_client_example():
    """Example WebSocket client."""
    
    # Connect to WebSocket server
    ws = connect_websocket("localhost", 8765)
    
    try:
        # Send messages
        ws.send("Hello WebSocket!")
        ws.send("How are you?")
        
        # Receive responses
        for _ in range(2):
            response = ws.recv()
            print(f"Server response: {response}")
            
        # Send JSON data
        import json
        data = {"type": "message", "content": "JSON message", "timestamp": time.time()}
        ws.send(json.dumps(data))
        
        response = ws.recv()
        print(f"JSON response: {response}")
        
    finally:
        ws.close()

# Run the client
websocket_client_example()
```

## Asynchronous WebSocket

### Async WebSocket Server

```python
import asyncio
from kn_sock import start_async_websocket_server

async def handle_async_websocket(websocket, path):
    """
    Handle async WebSocket connections.
    
    Args:
        websocket: The WebSocket connection
        path: The requested path
    """
    print(f"Async WebSocket client connected: {path}")
    
    try:
        async for message in websocket:
            print(f"Received: {message}")
            
            # Process the message
            if message.startswith("ping"):
                await websocket.send("pong")
            elif message.startswith("echo"):
                await websocket.send(f"Echo: {message[5:]}")
            else:
                await websocket.send(f"Processed: {message}")
                
    except Exception as e:
        print(f"Error in async handler: {e}")

# Start async WebSocket server
async def main():
    server = await start_async_websocket_server(
        "localhost", 8765, handle_async_websocket
    )
    print("Async WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

# Run the server
asyncio.run(main())
```

### Async WebSocket Client

```python
import asyncio
from kn_sock import async_connect_websocket

async def async_websocket_client():
    """Example async WebSocket client."""
    
    # Connect to async WebSocket server
    async with async_connect_websocket("localhost", 8765) as websocket:
        
        # Send multiple messages
        messages = ["ping", "echo Hello", "async message"]
        
        for message in messages:
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Response: {response}")
            
            # Small delay between messages
            await asyncio.sleep(0.5)

# Run the async client
asyncio.run(async_websocket_client())
```

## Related Topics

- **[TCP Protocol](tcp.md)** - For reliable JSON communication
- **[UDP Protocol](udp.md)** - For fast JSON messaging
- **[File Transfer](file-transfer.md)** - For large data transfer
- **[API Reference](../api-reference.md)** - Complete function documentation 