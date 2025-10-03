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
## See Also

- **[TCP Protocol](../protocols/tcp.md)** - For reliable message transport
- **[JSON Communication](../protocols/json.md)** - For structured message data  
- **[WebSocket Protocol](../protocols/websocket.md)** - For real-time communication
- **[RPC](rpc.md)** - For remote procedure calls
- **[Examples](../examples.md)** - Complete PubSub application examples
