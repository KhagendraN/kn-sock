# Publish/Subscribe Messaging

kn-sock provides a simple and efficient publish/subscribe (pub/sub) messaging system for decoupled communication between applications.

## Overview

Pub/Sub features in kn-sock:
- **Topic-based messaging**: Organize messages by topics
- **Multiple subscribers**: Many clients can subscribe to the same topic
- **Threading support**: Multi-threaded server for concurrent connections
- **Custom message handlers**: Process messages with custom logic
- **JSON-based protocol**: Simple JSON message format
- **TCP-based**: Reliable TCP connections for message delivery

## Basic Pub/Sub Usage

### Starting a PubSub Server

```python
from kn_sock import start_pubsub_server
import threading

def custom_handler(data, client_sock, server):
    """
    Custom handler for pubsub messages.
    
    Args:
        data (dict): The parsed message data from client
        client_sock (socket.socket): The client socket
        server (PubSubServer): The pubsub server instance
    """
    action = data.get("action")
    topic = data.get("topic", "unknown")
    
    if action == "subscribe":
        print(f"📝 Client subscribed to topic: {topic}")
    elif action == "unsubscribe":
        print(f"📤 Client unsubscribed from topic: {topic}")
    elif action == "publish":
        message = data.get("message", "")
        print(f"📢 Message published to '{topic}': {message}")

# Start the PubSub server
def start_server():
    print("🚀 Starting PubSub server on port 8080...")
    start_pubsub_server(
        port=8080,
        host='0.0.0.0',
        handler_func=custom_handler  # Optional custom handler
    )

# Start server in background thread (optional)
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

print("✅ PubSub server started!")
print("🔄 Server is running...")
```

### Publishing Messages

```python
from kn_sock import PubSubClient

def publisher_example():
    """Example of publishing messages to topics."""
    
    try:
        # Connect to the PubSub server
        client = PubSubClient("localhost", 8080)
        print("✅ Connected to PubSub server")
        
        # Publish messages to different topics
        client.publish("news/technology", "New AI breakthrough announced!")
        client.publish("news/sports", "Championship game tonight")
        client.publish("alerts/system", "Server maintenance scheduled")
        
        # Publish JSON data
        import json
        data = {
            "event": "order_created",
            "order_id": "ORD-789",
            "amount": 99.99,
            "customer": "john@example.com"
        }
        client.publish("orders/created", json.dumps(data))
        
        print("📤 All messages published successfully!")
        
    except Exception as e:
        print(f"❌ Error publishing messages: {e}")
    finally:
        client.close()

# Run the publisher
publisher_example()
```

### Subscribing to Messages

```python
from kn_sock import PubSubClient
import threading
import time

def subscriber_example():
    """Example of subscribing to topics and receiving messages."""
    
    def handle_messages(client):
        """Handle incoming messages in a separate thread."""
        try:
            while True:
                message = client.recv(timeout=1.0)
                if message:
                    topic = message.get("topic")
                    content = message.get("message")
                    print(f"📨 Received on '{topic}': {content}")
        except Exception as e:
            print(f"Message handler error: {e}")
    
    try:
        # Connect to the PubSub server
        client = PubSubClient("localhost", 8080)
        print("✅ Connected to PubSub server")
        
        # Subscribe to topics
        client.subscribe("news/technology")
        client.subscribe("news/sports") 
        client.subscribe("alerts/system")
        client.subscribe("orders/created")
        
        print("📡 Subscribed to topics, listening for messages...")
        
        # Start message handler in background thread
        listener_thread = threading.Thread(target=handle_messages, args=(client,), daemon=True)
        listener_thread.start()
        
        # Keep the subscriber running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down subscriber...")
            
    except Exception as e:
        print(f"❌ Subscriber error: {e}")
    finally:
        client.close()

# Run the subscriber
subscriber_example()
```
## Complete Working Example

Here's a complete example that demonstrates both server and client usage:

```python
#!/usr/bin/env python3
"""
Complete PubSub Example - Server and Client
"""

from kn_sock import start_pubsub_server, PubSubClient
import threading
import time
import json

def custom_handler(data, client_sock, server):
    """Custom handler for server-side message processing."""
    action = data.get("action")
    topic = data.get("topic", "unknown")
    
    if action == "subscribe":
        print(f"[SERVER] 📝 Client subscribed to: {topic}")
    elif action == "unsubscribe":
        print(f"[SERVER] 📤 Client unsubscribed from: {topic}")
    elif action == "publish":
        message = data.get("message", "")
        print(f"[SERVER] 📢 Message on '{topic}': {message}")

def start_pubsub_server_example():
    """Start the PubSub server."""
    print("🚀 Starting PubSub server on port 8080...")
    start_pubsub_server(
        port=8080,
        host='0.0.0.0',
        handler_func=custom_handler
    )

def publisher_client():
    """Publisher client example."""
    time.sleep(1)  # Wait for server to start
    
    try:
        client = PubSubClient("localhost", 8080)
        print("[PUBLISHER] ✅ Connected to server")
        
        # Publish some messages
        messages = [
            ("news", "Breaking news: kn-sock PubSub is working!"),
            ("alerts", "System maintenance at midnight"),
            ("data", json.dumps({"sensor_id": "temp_01", "value": 23.5}))
        ]
        
        for topic, message in messages:
            client.publish(topic, message)
            print(f"[PUBLISHER] 📤 Published to '{topic}': {message}")
            time.sleep(0.5)
            
    except Exception as e:
        print(f"[PUBLISHER] ❌ Error: {e}")
    finally:
        client.close()
        print("[PUBLISHER] 🔒 Connection closed")

def subscriber_client():
    """Subscriber client example."""
    time.sleep(1.5)  # Wait for server to start
    
    def message_listener(client):
        """Listen for messages."""
        while True:
            try:
                message = client.recv(timeout=1.0)
                if message:
                    topic = message.get("topic")
                    content = message.get("message")
                    print(f"[SUBSCRIBER] 📨 Received on '{topic}': {content}")
            except:
                break
    
    try:
        client = PubSubClient("localhost", 8080)
        print("[SUBSCRIBER] ✅ Connected to server")
        
        # Subscribe to topics
        topics = ["news", "alerts", "data"]
        for topic in topics:
            client.subscribe(topic)
            print(f"[SUBSCRIBER] 📡 Subscribed to: {topic}")
        
        # Start message listener
        listener_thread = threading.Thread(target=message_listener, args=(client,), daemon=True)
        listener_thread.start()
        
        # Keep subscriber alive for a while
        time.sleep(5)
        
    except Exception as e:
        print(f"[SUBSCRIBER] ❌ Error: {e}")
    finally:
        client.close()
        print("[SUBSCRIBER] 🔒 Connection closed")

def main():
    """Run the complete example."""
    print("=" * 50)
    print("kn-sock PubSub Complete Example")
    print("=" * 50)
    
    # Start server in background
    server_thread = threading.Thread(target=start_pubsub_server_example, daemon=True)
    server_thread.start()
    
    # Start subscriber in background
    subscriber_thread = threading.Thread(target=subscriber_client, daemon=True)
    subscriber_thread.start()
    
    # Start publisher
    publisher_thread = threading.Thread(target=publisher_client, daemon=True)
    publisher_thread.start()
    
    # Wait for clients to finish
    publisher_thread.join()
    subscriber_thread.join()
    
    print("\n✅ Example completed successfully!")
    print("💡 The server is still running in the background.")

if __name__ == "__main__":
    main()
```

## CLI Usage

You can also use kn-sock from the command line for quick testing:

```bash
# Start a PubSub server (in one terminal)
python -c "from kn_sock import start_pubsub_server; start_pubsub_server(8080)"

# Publish a message (in another terminal)
kn-sock pubsub-client localhost 8080 news "Hello World!"

# Subscribe to messages (in another terminal)  
kn-sock pubsub-client localhost 8080 news
```

## Message Protocol

Messages are sent as JSON over TCP, terminated with newlines:

### Subscribe Message
```json
{"action": "subscribe", "topic": "topic_name"}
```

### Unsubscribe Message  
```json
{"action": "unsubscribe", "topic": "topic_name"}
```

### Publish Message
```json
{"action": "publish", "topic": "topic_name", "message": "content"}
```

### Received Message (from server to subscriber)
```json
{"topic": "topic_name", "message": "content"}
```

## Best Practices

### Error Handling
Always wrap PubSub operations in try-catch blocks:

```python
from kn_sock import PubSubClient

def robust_publisher():
    client = None
    try:
        client = PubSubClient("localhost", 8080)
        client.publish("topic", "message")
    except ConnectionRefusedError:
        print("❌ Could not connect to PubSub server")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if client:
            client.close()
```

### Message Format Recommendations
Use consistent JSON structure for complex messages:

```python
import json
import time

# Good: Structured message format
message_data = {
    "timestamp": time.time(),
    "source": "sensor_01",
    "event_type": "temperature_reading",
    "data": {"temperature": 23.5, "unit": "celsius"},
    "metadata": {"location": "server_room", "priority": "normal"}
}

client.publish("sensors/temperature", json.dumps(message_data))
```

### Threading Considerations
When using multiple threads, ensure proper cleanup:

```python
import threading
import signal
import sys

class PubSubManager:
    def __init__(self):
        self.client = None
        self.running = True
        
    def start_subscriber(self):
        def message_loop():
            while self.running:
                try:
                    message = self.client.recv(timeout=1.0)
                    if message:
                        self.process_message(message)
                except Exception as e:
                    if self.running:  # Only log if not shutting down
                        print(f"Error: {e}")
        
        self.client = PubSubClient("localhost", 8080)
        self.client.subscribe("my_topic")
        
        thread = threading.Thread(target=message_loop, daemon=True)
        thread.start()
        return thread
    
    def stop(self):
        self.running = False
        if self.client:
            self.client.close()

# Graceful shutdown
manager = PubSubManager()
def signal_handler(sig, frame):
    manager.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
```

## Common Use Cases

### Real-time Notifications
```python
# Notification system
client = PubSubClient("localhost", 8080)

# Subscribe to user notifications
client.subscribe("notifications/user_123")

def notification_listener():
    while True:
        msg = client.recv()
        if msg:
            notification = json.loads(msg["message"])
            print(f"🔔 {notification['title']}: {notification['body']}")
```

### Event-driven Architecture
```python
# Order processing system
client = PubSubClient("localhost", 8080)

# Publish order events
def process_order(order_data):
    # Process the order
    order_id = order_data["id"]
    
    # Notify other services
    client.publish("orders/created", json.dumps({
        "order_id": order_id,
        "customer": order_data["customer"],
        "total": order_data["total"],
        "timestamp": time.time()
    }))
    
    # Later, when shipped...
    client.publish("orders/shipped", json.dumps({
        "order_id": order_id,
        "tracking_number": "TRK123456"
    }))
```

### Log Aggregation
```python
# Centralized logging
import logging

class PubSubLogHandler(logging.Handler):
    def __init__(self, host, port, topic):
        super().__init__()
        self.client = PubSubClient(host, port)
        self.topic = topic
    
    def emit(self, record):
        try:
            log_entry = {
                "level": record.levelname,
                "message": record.getMessage(),
                "timestamp": record.created,
                "module": record.module,
                "function": record.funcName
            }
            self.client.publish(self.topic, json.dumps(log_entry))
        except Exception:
            pass  # Don't fail the application due to logging errors

# Use the custom handler
logger = logging.getLogger("my_app")
pubsub_handler = PubSubLogHandler("localhost", 8080, "logs/my_app")
logger.addHandler(pubsub_handler)
```

## Troubleshooting

### Common Issues

**Connection Refused:**
- Ensure the PubSub server is running
- Check host and port configuration
- Verify firewall settings

**Messages Not Received:**
- Ensure subscriber is properly connected before publisher sends messages
- Check topic names for typos
- Verify the message listener thread is running

**High Memory Usage:**
- The server keeps client connections in memory
- Ensure clients properly call `close()` when done
- Monitor the number of concurrent connections

**Performance Tips:**
- Use threading for concurrent publishers/subscribers
- Batch multiple messages when possible  
- Consider message size - very large messages may cause delays
- Use specific topic names rather than broad patterns

## See Also

- **[TCP Protocol](../protocols/tcp.md)** - For reliable message transport
- **[JSON Communication](../protocols/json.md)** - For structured message data  
- **[WebSocket Protocol](../protocols/websocket.md)** - For real-time communication
- **[RPC](rpc.md)** - For remote procedure calls
- **[Examples](../examples.md)** - Complete PubSub application examples
