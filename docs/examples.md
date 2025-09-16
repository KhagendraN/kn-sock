# Examples

This page showcases real-world examples and complete applications built with kn-sock.

## Basic Examples

### Echo Server and Client

**Server:**
```python
from kn_sock import start_tcp_server

def echo_handler(data, addr, client_socket):
    message = data.decode('utf-8')
    print(f"Received from {addr}: {message}")
    response = f"Echo: {message}"
    client_socket.sendall(response.encode('utf-8'))

start_tcp_server(8080, echo_handler)
```

**Client:**
```python
from kn_sock import send_tcp_message

messages = ["Hello", "How are you?", "Goodbye"]
for message in messages:
    send_tcp_message("localhost", 8080, message)
```

### File Transfer

**Server:**
```python
from kn_sock import start_file_server
import os

def file_received_handler(filename, filepath, addr):
    file_size = os.path.getsize(filepath)
    print(f"File '{filename}' ({file_size} bytes) received from {addr}")

start_file_server(8080, "/tmp/received", handler=file_received_handler)
```

**Client:**
```python
from kn_sock import send_file

send_file("localhost", 8080, "/path/to/file.txt", show_progress=True)
```

## Advanced Examples

### Chat Application

**Server:**
```python
from kn_sock import start_websocket_server
import json

class ChatServer:
    def __init__(self):
        self.rooms = {}  # room_name -> set of clients
        self.clients = {}  # client_id -> (ws, room, nickname)
    
    def handle_client(self, ws):
        client_id = id(ws)
        try:
            while ws.open:
                message = ws.recv()
                if not message:
                    break
                
                data = json.loads(message)
                self.process_message(client_id, ws, data)
        finally:
            self.remove_client(client_id)
    
    def process_message(self, client_id, ws, data):
        msg_type = data.get('type')
        
        if msg_type == 'join':
            self.join_room(client_id, ws, data.get('room'), data.get('nickname'))
        elif msg_type == 'message':
            self.broadcast_message(client_id, data.get('message'))
    
    def join_room(self, client_id, ws, room, nickname):
        if room not in self.rooms:
            self.rooms[room] = set()
        
        self.rooms[room].add(client_id)
        self.clients[client_id] = (ws, room, nickname)
        
        # Notify others
        self.broadcast_to_room(room, {
            'type': 'user_joined',
            'nickname': nickname
        }, exclude_client=client_id)
    
    def broadcast_message(self, client_id, message):
        if client_id not in self.clients:
            return
        
        ws, room, nickname = self.clients[client_id]
        self.broadcast_to_room(room, {
            'type': 'message',
            'nickname': nickname,
            'message': message
        })
    
    def broadcast_to_room(self, room, data, exclude_client=None):
        if room not in self.rooms:
            return
        
        message = json.dumps(data)
        for client_id in self.rooms[room]:
            if client_id != exclude_client and client_id in self.clients:
                ws, _, _ = self.clients[client_id]
                try:
                    ws.send(message)
                except:
                    pass
    
    def remove_client(self, client_id):
        if client_id in self.clients:
            ws, room, nickname = self.clients[client_id]
            
            if room in self.rooms:
                self.rooms[room].discard(client_id)
            
            del self.clients[client_id]
            
            self.broadcast_to_room(room, {
                'type': 'user_left',
                'nickname': nickname
            })

server = ChatServer()
start_websocket_server("127.0.0.1", 8765, server.handle_client)
```

**Client:**
```python
from kn_sock import connect_websocket
import json
import threading

class ChatClient:
    def __init__(self, host, port, room, nickname):
        self.host = host
        self.port = port
        self.room = room
        self.nickname = nickname
        self.ws = None
        self.running = False
    
    def connect(self):
        self.ws = connect_websocket(self.host, self.port)
        
        join_message = {
            'type': 'join',
            'room': self.room,
            'nickname': self.nickname
        }
        self.ws.send(json.dumps(join_message))
    
    def start(self):
        self.connect()
        self.running = True
        
        # Start receive thread
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        # Main input loop
        try:
            while self.running:
                message = input()
                if message.lower() == 'quit':
                    break
                self.send_message(message)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
    
    def send_message(self, message):
        if self.ws and self.ws.open:
            data = {'type': 'message', 'message': message}
            self.ws.send(json.dumps(data))
    
    def receive_messages(self):
        while self.running and self.ws and self.ws.open:
            try:
                message = self.ws.recv()
                if not message:
                    break
                
                data = json.loads(message)
                self.handle_message(data)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
    
    def handle_message(self, data):
        msg_type = data.get('type')
        
        if msg_type == 'message':
            nickname = data.get('nickname')
            message = data.get('message')
            print(f"[{nickname}]: {message}")
        elif msg_type == 'user_joined':
            nickname = data.get('nickname')
            print(f"*** {nickname} joined the room ***")
        elif msg_type == 'user_left':
            nickname = data.get('nickname')
            print(f"*** {nickname} left the room ***")
    
    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()

# Usage
client = ChatClient("localhost", 8765, "general", "alice")
client.start()
```

### IoT Device Simulator

**Device:**
```python
from kn_sock import send_json
import random
import time

class IoTDevice:
    def __init__(self, device_id, server_host, server_port):
        self.device_id = device_id
        self.server_host = server_host
        self.server_port = server_port
    
    def generate_sensor_data(self):
        return {
            'device_id': self.device_id,
            'timestamp': time.time(),
            'temperature': random.uniform(20, 30),
            'humidity': random.uniform(40, 80),
            'pressure': random.uniform(1000, 1020)
        }
    
    def start(self, interval=5):
        print(f"IoT Device {self.device_id} started")
        
        try:
            while True:
                data = self.generate_sensor_data()
                try:
                    send_json(self.server_host, self.server_port, data)
                    print(f"✓ Data sent: {data['temperature']:.1f}°C")
                except Exception as e:
                    print(f"✗ Failed to send data: {e}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Device stopped")

# Usage
device = IoTDevice("sensor001", "localhost", 8080)
device.start()
```

**Server:**
```python
from kn_sock import start_json_server
import json
import time

class IoTServer:
    def __init__(self):
        self.devices = {}
    
    def handle_device_data(self, data, addr, client_socket):
        device_id = data.get('device_id')
        self.devices[device_id] = {
            'data': data,
            'last_seen': time.time(),
            'address': addr
        }
        
        # Check for alerts
        alerts = self.check_alerts(data)
        
        response = {
            'status': 'received',
            'device_id': device_id,
            'alerts': alerts
        }
        client_socket.sendall(json.dumps(response).encode('utf-8'))
        
        print(f"📊 Data from {device_id}: {data['temperature']:.1f}°C")
    
    def check_alerts(self, data):
        alerts = []
        
        if data['temperature'] > 28:
            alerts.append(f"High temperature: {data['temperature']:.1f}°C")
        elif data['temperature'] < 22:
            alerts.append(f"Low temperature: {data['temperature']:.1f}°C")
        
        return alerts

server = IoTServer()
start_json_server(8080, server.handle_device_data)
```

### Secure File Transfer

**Server:**
```python
from kn_sock import start_ssl_tcp_server
import os

def handle_secure_file_transfer(data, addr, client_socket):
    filename = data.decode().strip()
    
    try:
        with open(filename, 'rb') as f:
            file_data = f.read()
        
        # Send file size first
        size_msg = f"SIZE:{len(file_data)}".encode()
        client_socket.sendall(size_msg)
        
        # Send file data
        client_socket.sendall(file_data)
        
    except FileNotFoundError:
        error_msg = "ERROR:File not found".encode()
        client_socket.sendall(error_msg)

start_ssl_tcp_server(
    8443,
    handle_secure_file_transfer,
    certfile="server.crt",
    keyfile="server.key"
)
```

**Client:**
```python
from kn_sock import send_ssl_tcp_message
import os

def request_file(host, port, filename):
    try:
        # Request file
        send_ssl_tcp_message(host, port, filename)
        print(f"Requested file: {filename}")
    except Exception as e:
        print(f"Error requesting file: {e}")

# Usage
request_file("localhost", 8443, "document.pdf")
```

## Running Examples

### Prerequisites

```bash
pip install kn-sock
# For video/audio examples:
pip install opencv-python pyaudio numpy
```

### Quick Start

1. **Echo Server:**
   ```bash
   # Terminal 1
   python echo_server.py
   
   # Terminal 2
   python echo_client.py
   ```

2. **Chat Application:**
   ```bash
   # Terminal 1
   python chat_server.py
   
   # Terminal 2
   python chat_client.py localhost general alice
   
   # Terminal 3
   python chat_client.py localhost general bob
   ```

3. **IoT System:**
   ```bash
   # Terminal 1
   python iot_server.py
   
   # Terminal 2
   python iot_device.py
   ```

## Related Topics

- **[Getting Started](getting-started.md)** - For basic setup and usage
- **[API Reference](api-reference.md)** - For detailed function documentation
- **[CLI Guide](cli.md)** - For command-line examples 