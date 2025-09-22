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

## Advanced WebSocket Features

### WebSocket with Custom Protocol

```python
from kn_sock import start_websocket_server

class ChatProtocol:
    """Custom chat protocol for WebSocket."""
    
    def __init__(self):
        self.clients = {}
        self.rooms = {}
    
    def handle_client(self, client_socket, address):
        """Handle client with custom protocol."""
        client_id = f"{address[0]}:{address[1]}"
        self.clients[client_id] = client_socket
        
        try:
            # Send welcome message
            welcome = {
                "type": "welcome",
                "client_id": client_id,
                "message": "Connected to chat server"
            }
            client_socket.send(json.dumps(welcome))
            
            while True:
                message = client_socket.recv()
                if not message:
                    break
                    
                try:
                    data = json.loads(message)
                    self.process_message(client_id, data)
                except json.JSONDecodeError:
                    self.send_error(client_socket, "Invalid JSON format")
                    
        except Exception as e:
            print(f"Error with client {client_id}: {e}")
        finally:
            self.cleanup_client(client_id)
    
    def process_message(self, client_id, data):
        """Process incoming message based on type."""
        message_type = data.get("type")
        
        if message_type == "join_room":
            self.join_room(client_id, data.get("room"))
        elif message_type == "leave_room":
            self.leave_room(client_id, data.get("room"))
        elif message_type == "chat_message":
            self.broadcast_message(client_id, data)
        elif message_type == "private_message":
            self.send_private_message(client_id, data)
        else:
            self.send_error(self.clients[client_id], f"Unknown message type: {message_type}")
    
    def join_room(self, client_id, room_name):
        """Add client to a chat room."""
        if room_name not in self.rooms:
            self.rooms[room_name] = set()
        
        self.rooms[room_name].add(client_id)
        
        # Notify client
        response = {
            "type": "room_joined",
            "room": room_name,
            "members": len(self.rooms[room_name])
        }
        self.clients[client_id].send(json.dumps(response))
        
        # Notify other room members
        notification = {
            "type": "user_joined",
            "user": client_id,
            "room": room_name
        }
        self.broadcast_to_room(room_name, notification, exclude=client_id)
    
    def broadcast_message(self, sender_id, data):
        """Broadcast message to room members."""
        room_name = data.get("room")
        message = data.get("message")
        
        if room_name not in self.rooms or sender_id not in self.rooms[room_name]:
            self.send_error(self.clients[sender_id], "Not in specified room")
            return
        
        broadcast_data = {
            "type": "chat_message",
            "sender": sender_id,
            "room": room_name,
            "message": message,
            "timestamp": time.time()
        }
        
        self.broadcast_to_room(room_name, broadcast_data)
    
    def broadcast_to_room(self, room_name, data, exclude=None):
        """Broadcast data to all clients in a room."""
        if room_name not in self.rooms:
            return
        
        message = json.dumps(data)
        for client_id in self.rooms[room_name]:
            if client_id != exclude and client_id in self.clients:
                try:
                    self.clients[client_id].send(message)
                except Exception as e:
                    print(f"Error sending to {client_id}: {e}")
                    self.cleanup_client(client_id)
    
    def send_error(self, client_socket, error_message):
        """Send error message to client."""
        error_data = {
            "type": "error",
            "message": error_message
        }
        client_socket.send(json.dumps(error_data))
    
    def cleanup_client(self, client_id):
        """Clean up client from all data structures."""
        # Remove from all rooms
        for room_name, members in self.rooms.items():
            if client_id in members:
                members.remove(client_id)
                
                # Notify remaining room members
                notification = {
                    "type": "user_left",
                    "user": client_id,
                    "room": room_name
                }
                self.broadcast_to_room(room_name, notification)
        
        # Remove from clients
        if client_id in self.clients:
            del self.clients[client_id]

# Use the custom protocol
protocol = ChatProtocol()
start_websocket_server("localhost", 8765, protocol.handle_client)
```

### WebSocket with Heartbeat

```python
import threading
import time
from kn_sock import start_websocket_server

class HeartbeatWebSocketServer:
    """WebSocket server with heartbeat monitoring."""
    
    def __init__(self):
        self.clients = {}
        self.heartbeat_interval = 30  # seconds
        self.heartbeat_timeout = 60   # seconds
        self.running = True
        
        # Start heartbeat monitor thread
        threading.Thread(target=self.heartbeat_monitor, daemon=True).start()
    
    def handle_client(self, client_socket, address):
        """Handle client with heartbeat monitoring."""
        client_id = f"{address[0]}:{address[1]}"
        
        # Register client
        self.clients[client_id] = {
            "socket": client_socket,
            "last_ping": time.time(),
            "connected": True
        }
        
        print(f"Client {client_id} connected")
        
        try:
            while self.clients[client_id]["connected"]:
                message = client_socket.recv(timeout=1.0)  # Non-blocking receive
                
                if message:
                    if message == "pong":
                        # Update last ping time
                        self.clients[client_id]["last_ping"] = time.time()
                        print(f"Received pong from {client_id}")
                    else:
                        # Process regular message
                        print(f"Message from {client_id}: {message}")
                        client_socket.send(f"Echo: {message}")
                        
        except Exception as e:
            print(f"Error with client {client_id}: {e}")
        finally:
            self.cleanup_client(client_id)
    
    def heartbeat_monitor(self):
        """Monitor client heartbeats and send pings."""
        while self.running:
            current_time = time.time()
            
            # Check all clients
            dead_clients = []
            for client_id, client_info in self.clients.items():
                last_ping = client_info["last_ping"]
                
                # Check if client is unresponsive
                if current_time - last_ping > self.heartbeat_timeout:
                    print(f"Client {client_id} timed out")
                    dead_clients.append(client_id)
                
                # Send ping if needed
                elif current_time - last_ping > self.heartbeat_interval:
                    try:
                        client_info["socket"].send("ping")
                        print(f"Sent ping to {client_id}")
                    except Exception as e:
                        print(f"Failed to ping {client_id}: {e}")
                        dead_clients.append(client_id)
            
            # Clean up dead clients
            for client_id in dead_clients:
                self.cleanup_client(client_id)
            
            time.sleep(5)  # Check every 5 seconds
    
    def cleanup_client(self, client_id):
        """Clean up disconnected client."""
        if client_id in self.clients:
            self.clients[client_id]["connected"] = False
            try:
                self.clients[client_id]["socket"].close()
            except:
                pass
            del self.clients[client_id]
            print(f"Client {client_id} cleaned up")

# Start heartbeat server
server = HeartbeatWebSocketServer()
start_websocket_server("localhost", 8765, server.handle_client)
```

## WebSocket Client Patterns

### Reconnecting WebSocket Client

```python
import time
import threading
from kn_sock import connect_websocket

class ReconnectingWebSocketClient:
    """WebSocket client with automatic reconnection."""
    
    def __init__(self, host, port, reconnect_interval=5):
        self.host = host
        self.port = port
        self.reconnect_interval = reconnect_interval
        self.websocket = None
        self.connected = False
        self.running = True
        self.message_queue = []
        
    def connect(self):
        """Connect to WebSocket server."""
        try:
            self.websocket = connect_websocket(self.host, self.port)
            self.connected = True
            print(f"Connected to WebSocket server at {self.host}:{self.port}")
            
            # Send queued messages
            self.send_queued_messages()
            
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from WebSocket server."""
        self.running = False
        self.connected = False
        
        if self.websocket:
            try:
                self.websocket.close()
            except:
                pass
            self.websocket = None
    
    def send_message(self, message):
        """Send message to server (queue if not connected)."""
        if self.connected and self.websocket:
            try:
                self.websocket.send(message)
                return True
            except Exception as e:
                print(f"Failed to send message: {e}")
                self.connected = False
                self.message_queue.append(message)
                return False
        else:
            # Queue message for later
            self.message_queue.append(message)
            return False
    
    def send_queued_messages(self):
        """Send all queued messages."""
        while self.message_queue and self.connected:
            message = self.message_queue.pop(0)
            if not self.send_message(message):
                # Re-queue if sending fails
                self.message_queue.insert(0, message)
                break
    
    def receive_messages(self):
        """Receive messages in a loop."""
        while self.running:
            if self.connected and self.websocket:
                try:
                    message = self.websocket.recv(timeout=1.0)
                    if message:
                        self.handle_message(message)
                except Exception as e:
                    print(f"Error receiving message: {e}")
                    self.connected = False
            else:
                time.sleep(0.1)
    
    def handle_message(self, message):
        """Handle received message (override in subclass)."""
        print(f"Received: {message}")
    
    def run(self):
        """Main client loop with automatic reconnection."""
        # Start receive thread
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        while self.running:
            if not self.connected:
                print("Attempting to connect...")
                if self.connect():
                    continue
                else:
                    print(f"Reconnecting in {self.reconnect_interval} seconds...")
                    time.sleep(self.reconnect_interval)
            else:
                time.sleep(1)

# Usage example
client = ReconnectingWebSocketClient("localhost", 8765)

# Start client in background
client_thread = threading.Thread(target=client.run, daemon=True)
client_thread.start()

# Send messages
for i in range(10):
    client.send_message(f"Message {i}")
    time.sleep(2)

# Cleanup
client.disconnect()
```

## WebSocket Security

### Secure WebSocket (WSS)

```python
import ssl
from kn_sock import start_websocket_server

def secure_websocket_server():
    """Start a secure WebSocket server with SSL/TLS."""
    
    def handle_secure_client(client_socket, address):
        print(f"Secure WebSocket client connected from {address}")
        
        try:
            while True:
                message = client_socket.recv()
                if not message:
                    break
                
                print(f"Secure message: {message}")
                client_socket.send(f"Secure echo: {message}")
                
        except Exception as e:
            print(f"Error in secure handler: {e}")
        finally:
            client_socket.close()
    
    # SSL configuration
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain("server.crt", "server.key")
    
    # Start secure server
    start_websocket_server(
        "localhost", 8765, 
        handle_secure_client,
        ssl_context=ssl_context
    )

# Connect to secure WebSocket
from kn_sock import connect_websocket

def secure_websocket_client():
    """Connect to secure WebSocket server."""
    
    # SSL configuration for client
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False  # For self-signed certificates
    ssl_context.verify_mode = ssl.CERT_NONE
    
    ws = connect_websocket(
        "localhost", 8765,
        ssl_context=ssl_context
    )
    
    ws.send("Secure message")
    response = ws.recv()
    print(f"Secure response: {response}")
    
    ws.close()
```

## Performance Optimization

### Connection Pooling

```python
import queue
import threading
from kn_sock import connect_websocket

class WebSocketPool:
    """WebSocket connection pool for high-performance clients."""
    
    def __init__(self, host, port, pool_size=10):
        self.host = host
        self.port = port
        self.pool_size = pool_size
        self.pool = queue.Queue()
        self.lock = threading.Lock()
        
        # Create initial connections
        self.create_pool()
    
    def create_pool(self):
        """Create initial pool of connections."""
        for _ in range(self.pool_size):
            try:
                ws = connect_websocket(self.host, self.port)
                self.pool.put(ws)
            except Exception as e:
                print(f"Failed to create pooled connection: {e}")
    
    def get_connection(self, timeout=10):
        """Get a connection from the pool."""
        try:
            return self.pool.get(timeout=timeout)
        except queue.Empty:
            # Create new connection if pool is empty
            return connect_websocket(self.host, self.port)
    
    def return_connection(self, ws):
        """Return a connection to the pool."""
        if self.pool.qsize() < self.pool_size:
            self.pool.put(ws)
        else:
            # Pool is full, close the connection
            ws.close()
    
    def send_message(self, message):
        """Send message using pooled connection."""
        ws = self.get_connection()
        try:
            ws.send(message)
            response = ws.recv()
            return response
        finally:
            self.return_connection(ws)
    
    def close_all(self):
        """Close all pooled connections."""
        while not self.pool.empty():
            try:
                ws = self.pool.get_nowait()
                ws.close()
            except queue.Empty:
                break

# Usage
pool = WebSocketPool("localhost", 8765, pool_size=5)

# Send multiple messages efficiently
for i in range(100):
    response = pool.send_message(f"Pooled message {i}")
    print(f"Response {i}: {response}")

pool.close_all()
```

## Troubleshooting

### Common WebSocket Issues

#### Connection Refused
```python
try:
    ws = connect_websocket("localhost", 8765)
except ConnectionRefusedError:
    print("WebSocket server is not running or port is incorrect")
```

#### Handshake Failure
```python
try:
    ws = connect_websocket("localhost", 8765, resource="/ws")
except Exception as e:
    if "handshake" in str(e).lower():
        print("WebSocket handshake failed - check server configuration")
```

#### Message Size Limits
```python
# Configure maximum message size
ws = connect_websocket("localhost", 8765, max_size=1024*1024)  # 1MB
```

### Debugging WebSocket Connections

```python
import logging

# Enable WebSocket debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('websocket')

def debug_websocket_handler(client_socket, address):
    """Debug WebSocket handler with detailed logging."""
    logger.info(f"Client connected: {address}")
    
    try:
        while True:
            message = client_socket.recv()
            if not message:
                logger.info(f"Client {address} disconnected")
                break
            
            logger.debug(f"Received from {address}: {message}")
            response = f"Debug echo: {message}"
            client_socket.send(response)
            logger.debug(f"Sent to {address}: {response}")
            
    except Exception as e:
        logger.error(f"Error with client {address}: {e}")
    finally:
        client_socket.close()
        logger.info(f"Closed connection to {address}")
```

## See Also

- **[TCP Protocol](tcp.md)** - For reliable connection-based communication
- **[JSON Communication](json.md)** - For structured data over WebSockets
- **[Real-time Examples](../examples.md)** - WebSocket application examples
- **[Advanced Features](../advanced/)** - Live streaming and video chat
- **[Troubleshooting](../troubleshooting.md)** - Common issues and solutions
