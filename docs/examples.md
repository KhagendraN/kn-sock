# Examples

This page showcases real-world examples and complete applications built with kn-sock.

## Basic Examples

### Auto-Detect Network and Scan

```python
from kn_sock.network import arp_scan
from kn_sock.network.arp import get_local_network_info

def smart_network_scan():
    """Automatically detect and scan local network."""
    # Get local network information
    info = get_local_network_info()
    print(f"Local IP: {info['local_ip']}")
    print(f"Interface: {info['interface']}")
    print(f"Gateway: {info['gateway']}")
    
    # Auto-generate network range
    local_ip = info['local_ip']
    if local_ip != "Unknown" and '.' in local_ip:
        ip_parts = local_ip.split('.')
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        
        print(f"\nScanning network: {network_range}")
        devices = arp_scan(network_range, verbose=True)
        
        if devices:
            print(f"\n✅ Found {len(devices)} devices:")
            print("-" * 50)
            for i, device in enumerate(devices, 1):
                print(f"{i:2d}. IP: {device['ip']:15s} MAC: {device['mac']}")
        else:
            print("No devices found on this network.")
    else:
        print("Could not auto-detect network. Please specify manually.")

if __name__ == "__main__":
    smart_network_scan()
```

### Simple Network Inventory

```python
from kn_sock.network import arp_scan

def network_inventory(network_range="192.168.1.0/24"):
    """Create a simple network inventory."""
    try:
        devices = arp_scan(network_range, verbose=True)
        
        print(f"Network Inventory - Found {len(devices)} devices:")
        print("-" * 50)
        
        for i, device in enumerate(devices, 1):
            print(f"{i:2d}. IP: {device['ip']:15s} MAC: {device['mac']}")
            
    except RuntimeError as e:
        if "Operation not permitted" in str(e):
            print("❌ ARP scan requires root privileges. Run with sudo:")
            print("sudo python your_script.py")
        else:
            print(f"❌ Scan failed: {e}")

if __name__ == "__main__":
    network_inventory()
```

### Continuous Network Monitoring

```python
import time
from kn_sock.network import arp_scan
from kn_sock.network.arp import get_local_network_info

def monitor_network():
    """Monitor network for device changes."""
    # Auto-detect network range
    info = get_local_network_info()
    local_ip = info['local_ip']
    
    if local_ip == "Unknown":
        print("❌ Could not detect local network. Please specify manually.")
        return
    
    ip_parts = local_ip.split('.')
    network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    
    print(f"Monitoring network: {network_range}")
    print("Press Ctrl+C to stop monitoring\n")
    
    known_devices = set()
    scan_count = 0
    
    try:
        while True:
            scan_count += 1
            print(f"[Scan #{scan_count}] Checking network...")
            
            try:
                current_devices = arp_scan(network_range)
                current_ips = {device['ip'] for device in current_devices}
                
                # Find new devices
                new_devices = current_ips - known_devices
                if new_devices:
                    print(f"🔍 New devices detected: {new_devices}")
                
                # Find disconnected devices
                disconnected = known_devices - current_ips
                if disconnected:
                    print(f"📤 Devices disconnected: {disconnected}")
                
                known_devices = current_ips
                print(f"✅ Currently active: {len(current_ips)} devices")
                
            except Exception as e:
                print(f"❌ Scan failed: {e}")
            
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        print(f"\nMonitoring stopped after {scan_count} scans.")

if __name__ == "__main__":
    monitor_network()
```

### Integration with MAC Lookup

```python
from kn_sock.network import arp_scan, mac_lookup
from kn_sock.network.arp import get_local_network_info

def detailed_network_scan():
    """Scan network and identify device vendors."""
    # Auto-detect network
    info = get_local_network_info()
    local_ip = info['local_ip']
    
    if local_ip == "Unknown":
        network_range = "192.168.1.0/24"  # Fallback
        print(f"Using fallback network range: {network_range}")
    else:
        ip_parts = local_ip.split('.')
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        print(f"Scanning detected network: {network_range}")
    
    try:
        devices = arp_scan(network_range)
        
        if not devices:
            print("No devices found on network.")
            return
            
        print(f"\nDetailed Network Analysis - {len(devices)} devices found:")
        print("=" * 70)
        
        for i, device in enumerate(devices, 1):
            print(f"\n[Device #{i}]")
            print(f"IP Address: {device['ip']}")
            print(f"MAC Address: {device['mac']}")
            
            # Lookup vendor information
            try:
                vendor_info = mac_lookup(device['mac'], use_api=False)  # Use offline first
                print(f"Vendor: {vendor_info['vendor']}")
                print(f"OUI: {vendor_info['oui']}")
            except Exception as e:
                print(f"Vendor lookup failed: {e}")
            
            print("-" * 40)
            
    except Exception as e:
        if "Operation not permitted" in str(e):
            print("❌ Root privileges required. Run with: sudo python script.py")
        else:
            print(f"❌ Scan failed: {e}")

if __name__ == "__main__":
    detailed_network_scan()
```

### Network Device Inventory

```python
from kn_sock.network import arp_scan, mac_lookup
from kn_sock.network.arp import get_local_network_info

def device_inventory():
    """Create detailed device inventory with vendor information."""
    # Auto-detect network or use fallback
    info = get_local_network_info()
    local_ip = info['local_ip']
    
    if local_ip != "Unknown" and '.' in local_ip:
        ip_parts = local_ip.split('.')
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    else:
        network_range = "192.168.1.0/24"  # Fallback
        
    print(f"Scanning network: {network_range}")
    
    try:
        # Scan network for devices
        devices = arp_scan(network_range)
        
        if not devices:
            print("No devices found on network.")
            return
            
        print("\nNetwork Device Inventory")
        print("=" * 60)
        
        for i, device in enumerate(devices, 1):
            # Lookup vendor information
            try:
                vendor_info = mac_lookup(device['mac'], use_api=False)
                print(f"\n[Device #{i}]")
                print(f"IP Address: {device['ip']}")
                print(f"MAC Address: {device['mac']}")
                print(f"Vendor: {vendor_info['vendor']}")
                print(f"OUI: {vendor_info['oui']}")
                print("-" * 40)
            except Exception as e:
                print(f"Vendor lookup failed for {device['mac']}: {e}")
                
    except Exception as e:
        if "Operation not permitted" in str(e):
            print("❌ Root privileges required. Run with: sudo python script.py")
        else:
            print(f"❌ Network scan failed: {e}")

if __name__ == "__main__":
    device_inventory()
```

### Virtual Machine Detection

```python
from kn_sock.network import arp_scan, mac_lookup
from kn_sock.network.arp import get_local_network_info

def detect_virtual_machines():
    """Identify virtual machines on the network."""
    # Auto-detect network
    info = get_local_network_info()
    local_ip = info['local_ip']
    
    if local_ip != "Unknown" and '.' in local_ip:
        ip_parts = local_ip.split('.')
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    else:
        network_range = "192.168.1.0/24"
        
    vm_keywords = ["vmware", "virtualbox", "qemu", "microsoft", "xen", "oracle"]
    
    try:
        devices = arp_scan(network_range)
        
        if not devices:
            print("No devices found on network.")
            return
            
        print("Virtual Machine Detection")
        print("=" * 40)
        
        vms_found = 0
        for device in devices:
            try:
                vendor_info = mac_lookup(device['mac'], use_api=False)
                vendor_lower = vendor_info['vendor'].lower()
                
                is_vm = any(keyword in vendor_lower for keyword in vm_keywords)
                
                if is_vm:
                    print(f"🖥️  VM Detected: {device['ip']} ({vendor_info['vendor']})")
                    vms_found += 1
                else:
                    print(f"💻 Physical Device: {device['ip']} ({vendor_info['vendor']})")
                    
            except Exception as e:
                print(f"❌ Could not analyze {device['ip']}: {e}")
        
        print(f"\nSummary: Found {vms_found} virtual machines out of {len(devices)} devices.")
        
    except Exception as e:
        if "Operation not permitted" in str(e):
            print("❌ Root privileges required. Run with: sudo python script.py")
        else:
            print(f"❌ Scan failed: {e}")

if __name__ == "__main__":
    detect_virtual_machines()
```

### MAC Address Validation Tool

```python
from kn_sock.network.mac_lookup import validate_mac, mac_lookup

def validate_and_lookup():
    """Validate MAC addresses and lookup vendor information."""
    test_macs = [
        "00:1A:2B:3C:4D:5E",     # Valid colon format
        "00-50-56-C0-00-08",     # Valid hyphen format  
        "001A2B3C4D5E",          # Valid compact format
        "00:50:56:c0:00:08",     # Valid mixed case
        "00:1A:2B:3C:4D",        # Invalid - too short
        "invalid-mac-address"     # Invalid format
    ]
    
    print("MAC Address Validation and Lookup")
    print("=" * 50)
    
    for mac in test_macs:
        print(f"\nTesting: {mac}")
        
        if validate_mac(mac):
            try:
                result = mac_lookup(mac, use_api=False)
                print(f"  ✅ Status: Valid")
                print(f"  🏢 Vendor: {result['vendor']}")
                print(f"  🔖 OUI: {result['oui']}")
                print(f"  📍 Normalized: {result['mac']}")
            except Exception as e:
                print(f"  ✅ Status: Valid format")
                print(f"  ❌ Lookup failed: {e}")
        else:
            print(f"  ❌ Status: Invalid MAC address format")
        
        print("-" * 30)

if __name__ == "__main__":
    validate_and_lookup()
```

### Batch Processing with Error Handling

```python
from kn_sock.network.mac_lookup import batch_mac_lookup

def batch_lookup_with_errors():
    """Process multiple MAC addresses with error handling."""
    macs = [
        "00:1A:2B:3C:4D:5E",  # Valid
        "08:00:27:12:34:56",  # Valid
        "invalid-mac",        # Invalid
        "52:54:00:AB:CD:EF"   # Valid
    ]
    
    results = batch_mac_lookup(macs, use_api=False)
    
    print("Batch MAC Lookup Results")
    print("=" * 50)
    
    for i, result in enumerate(results):
        mac = macs[i]
        print(f"MAC: {mac}")
        
        if "Error" in result['vendor']:
            print(f"  Status: Error - {result['vendor']}")
        else:
            print(f"  Status: Success")
            print(f"  Vendor: {result['vendor']}")
            print(f"  OUI: {result['oui']}")
        
        print("-" * 30)

if __name__ == "__main__":
    batch_lookup_with_errors()
```

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

### Publish/Subscribe Messaging System

This example demonstrates a complete PubSub system with server, publishers, and subscribers.

**PubSub Server:**
```python
from kn_sock import start_pubsub_server
import threading

def message_handler(data, client_sock, server):
    """Custom handler to log all PubSub activities."""
    action = data.get("action")
    topic = data.get("topic", "unknown")
    
    if action == "subscribe":
        print(f"📝 Client subscribed to: {topic}")
    elif action == "unsubscribe":
        print(f"📤 Client unsubscribed from: {topic}")
    elif action == "publish":
        message = data.get("message", "")
        print(f"📢 Message on '{topic}': {message}")

# Start PubSub server
print("🚀 Starting PubSub server on port 8080...")
start_pubsub_server(
    port=8080,
    host='0.0.0.0',
    handler_func=message_handler
)
```

**Publisher Client:**
```python
from kn_sock import PubSubClient
import json
import time

def publish_news():
    """Publish news messages to different topics."""
    try:
        client = PubSubClient("localhost", 8080)
        print("✅ Publisher connected!")
        
        # Publish different types of news
        news_items = [
            ("news/tech", "AI breakthrough: New language model released"),
            ("news/sports", "Championship finals tonight at 8 PM"),
            ("alerts/system", "Server maintenance scheduled for midnight"),
            ("data/sensors", json.dumps({
                "sensor_id": "temp_01", 
                "temperature": 23.5, 
                "unit": "celsius"
            }))
        ]
        
        for topic, message in news_items:
            print(f"📤 Publishing to '{topic}': {message}")
            client.publish(topic, message)
            time.sleep(0.5)  # Small delay between messages
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    publish_news()
```

**Subscriber Client:**
```python
from kn_sock import PubSubClient
import threading
import time
import json

def create_subscriber(name, topics):
    """Create a subscriber for specific topics."""
    
    def message_listener(client):
        """Listen for messages in a separate thread."""
        while True:
            try:
                message = client.recv(timeout=1.0)
                if message:
                    topic = message.get("topic")
                    content = message.get("message")
                    print(f"[{name}] 📨 Received on '{topic}': {content}")
                    
                    # Try to parse JSON data
                    try:
                        parsed = json.loads(content)
                        if isinstance(parsed, dict):
                            print(f"[{name}] 📊 Data: {parsed}")
                    except:
                        pass  # Not JSON, that's fine
            except Exception as e:
                print(f"[{name}] ⚠️  Error: {e}")
                break
    
    try:
        # Connect to server
        client = PubSubClient("localhost", 8080)
        print(f"[{name}] ✅ Connected to PubSub server")
        
        # Subscribe to topics
        for topic in topics:
            client.subscribe(topic)
            print(f"[{name}] 📡 Subscribed to: {topic}")
        
        # Start message listener
        listener_thread = threading.Thread(
            target=message_listener, 
            args=(client,), 
            daemon=True
        )
        listener_thread.start()
        
        # Keep subscriber running
        time.sleep(10)  # Run for 10 seconds in demo
        
        # Unsubscribe
        for topic in topics:
            client.unsubscribe(topic)
        
        client.close()
        print(f"[{name}] 🔒 Disconnected")
        
    except Exception as e:
        print(f"[{name}] ❌ Error: {e}")

def main():
    """Run multiple subscribers for demo."""
    # Create different subscribers for different topic categories
    news_subscriber = threading.Thread(
        target=create_subscriber, 
        args=("NEWS_SUB", ["news/tech", "news/sports"]),
        daemon=True
    )
    
    system_subscriber = threading.Thread(
        target=create_subscriber,
        args=("SYS_SUB", ["alerts/system", "data/sensors"]),
        daemon=True
    )
    
    # Start subscribers
    news_subscriber.start()
    system_subscriber.start()
    
    # Wait for them to finish
    news_subscriber.join()
    system_subscriber.join()

if __name__ == "__main__":
    main()
```

**Complete Working Example:**

For a complete, ready-to-run example, see: [`docs/examples/pubsub_example.py`](pubsub_example.py)

```bash
# Run the complete example
python docs/examples/pubsub_example.py
```

This example includes:
- PubSub server with custom message handler
- Multiple publisher and subscriber clients
- JSON message parsing
- Proper error handling and cleanup
- Detailed logging of all activities

### Remote Procedure Call (RPC) System

This example demonstrates a complete RPC system with server and client.

**RPC Server:**
```python
from kn_sock import start_rpc_server

class MathService:
    """Example RPC service with mathematical operations."""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

def start_math_rpc_server():
    """Start a basic RPC server."""
    
    # Create service instance
    math_service = MathService()
    
    # Define additional functions
    def hello(name):
        return f"Hello, {name}!"
    
    def get_server_time():
        import datetime
        return datetime.datetime.now().isoformat()
    
    # Register all functions in a flat dictionary
    register_funcs = {
        # Math service methods
        'add': math_service.add,
        'subtract': math_service.subtract,
        'multiply': math_service.multiply,
        'divide': math_service.divide,
        
        # Standalone functions  
        'hello': hello,
        'get_time': get_server_time
    }
    
    print("🚀 Starting RPC Server on localhost:8080")
    print("📋 Available RPC methods:")
    for method_name in register_funcs.keys():
        print(f"  - {method_name}")
    
    # Start the RPC server
    start_rpc_server(
        port=8080,
        register_funcs=register_funcs,
        host='0.0.0.0'
    )

if __name__ == "__main__":
    start_math_rpc_server()
```

**RPC Client:**
```python
from kn_sock import RPCClient

def test_rpc_client():
    """Example RPC client."""
    
    client = None
    try:
        # Connect to RPC server
        client = RPCClient('localhost', 8080)
        print("✅ Connected to RPC server")
        
        # Call individual functions
        greeting = client.call('hello', 'Alice')
        print(f"Greeting: {greeting}")
        
        server_time = client.call('get_time')
        print(f"Server time: {server_time}")
        
        # Call math functions
        result = client.call('add', 10, 20)
        print(f"10 + 20 = {result}")
        
        result = client.call('multiply', 7, 8)
        print(f"7 * 8 = {result}")
        
        # Handle errors
        try:
            result = client.call('divide', 10, 0)
            print(f"10 / 0 = {result}")
        except Exception as e:
            print(f"Division by zero error: {e}")
        
        # Call non-existent method
        try:
            result = client.call('non_existent_method')
        except Exception as e:
            print(f"Method not found error: {e}")
        
    except ConnectionRefusedError:
        print("❌ Could not connect to RPC server. Is it running?")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if client is not None:
            client.close()
            print("🔒 Client connection closed")

if __name__ == "__main__":
    test_rpc_client()
```

**Complete Working Example:**

For a complete, ready-to-run example, see: [`docs/examples/rpc_example.py`](rpc_example.py)

```bash
# Run the complete example
python docs/examples/rpc_example.py
```

This example includes:
- RPC server with multiple services (math, utility functions)
- RPC client with comprehensive testing
- JSON-RPC protocol over TCP
- Error handling for division by zero and method not found
- Proper connection management and cleanup

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