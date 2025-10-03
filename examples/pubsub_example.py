#!/usr/bin/env python3
"""
Complete PubSub Working Example

This example demonstrates how to use kn-sock's PubSub functionality
with both server and client components.

To run this example:
1. python docs/examples/pubsub_example.py
2. Watch the output to see the complete workflow

This example includes:
- Starting a PubSub server with custom message handler
- Publishing messages from a client
- Subscribing to topics and receiving messages
- Proper error handling and resource cleanup
"""

from kn_sock import start_pubsub_server, PubSubClient
import threading
import time
import json
import sys

def custom_message_handler(data, client_sock, server):
    """
    Custom handler for server-side message processing.
    
    Args:
        data (dict): The parsed JSON message from client
        client_sock (socket.socket): The client socket connection  
        server (PubSubServer): The server instance
    """
    action = data.get("action")
    topic = data.get("topic", "unknown")
    
    if action == "subscribe":
        print(f"[SERVER] 📝 Client subscribed to: {topic}")
    elif action == "unsubscribe":
        print(f"[SERVER] 📤 Client unsubscribed from: {topic}")
    elif action == "publish":
        message = data.get("message", "")
        print(f"[SERVER] 📢 Message on '{topic}': {message}")

def start_pubsub_server_demo():
    """Start the PubSub server."""
    print("🚀 Starting PubSub server on port 8080...")
    try:
        start_pubsub_server(
            port=8080,
            host='0.0.0.0',
            handler_func=custom_message_handler
        )
    except Exception as e:
        print(f"[SERVER] ❌ Error starting server: {e}")

def publisher_demo():
    """Demonstrate publishing messages."""
    time.sleep(1)  # Wait for server to start
    
    try:
        print("[PUBLISHER] 🔌 Connecting to PubSub server...")
        client = PubSubClient("localhost", 8080)
        print("[PUBLISHER] ✅ Connected successfully!")
        
        # Publish various types of messages
        messages = [
            ("news/tech", "AI breakthrough: New language model released"),
            ("news/sports", "Championship finals tonight at 8 PM"),
            ("alerts/system", "System maintenance scheduled for midnight"),
            ("data/sensors", json.dumps({"sensor_id": "temp_01", "temperature": 23.5, "unit": "celsius"})),
            ("events/user", json.dumps({"user_id": "user_123", "action": "login", "timestamp": time.time()}))
        ]
        
        for topic, message in messages:
            print(f"[PUBLISHER] 📤 Publishing to '{topic}'...")
            client.publish(topic, message)
            time.sleep(0.3)  # Small delay between messages
        
        print("[PUBLISHER] ✅ All messages published successfully!")
        
    except ConnectionRefusedError:
        print("[PUBLISHER] ❌ Could not connect to server. Is it running?")
    except Exception as e:
        print(f"[PUBLISHER] ❌ Error: {e}")
    finally:
        client.close()
        print("[PUBLISHER] 🔒 Connection closed")

def subscriber_demo():
    """Demonstrate subscribing to topics and receiving messages."""
    time.sleep(1.5)  # Wait for server to start
    
    def message_listener(client, name):
        """Listen for messages in a separate thread."""
        try:
            while True:
                message = client.recv(timeout=1.0)
                if message:
                    topic = message.get("topic")
                    content = message.get("message")
                    print(f"[{name}] 📨 Received on '{topic}': {content}")
                    
                    # Parse JSON messages if possible
                    try:
                        parsed = json.loads(content)
                        if isinstance(parsed, dict):
                            print(f"[{name}] 📊 Parsed data: {parsed}")
                    except:
                        pass  # Not JSON, that's fine
        except Exception as e:
            print(f"[{name}] ⚠️  Message listener stopped: {e}")
    
    try:
        # Create two different subscribers to demonstrate multiple connections
        print("[SUBSCRIBER1] 🔌 Connecting to PubSub server...")
        client1 = PubSubClient("localhost", 8080)
        print("[SUBSCRIBER1] ✅ Connected!")
        
        print("[SUBSCRIBER2] 🔌 Connecting to PubSub server...")  
        client2 = PubSubClient("localhost", 8080)
        print("[SUBSCRIBER2] ✅ Connected!")
        
        # Subscribe to different topics
        print("[SUBSCRIBER1] 📡 Subscribing to news topics...")
        client1.subscribe("news/tech")
        client1.subscribe("news/sports")
        
        print("[SUBSCRIBER2] 📡 Subscribing to system topics...")
        client2.subscribe("alerts/system")
        client2.subscribe("data/sensors")
        client2.subscribe("events/user")
        
        # Start message listeners
        listener1 = threading.Thread(
            target=message_listener, 
            args=(client1, "SUBSCRIBER1"), 
            daemon=True
        )
        listener2 = threading.Thread(
            target=message_listener, 
            args=(client2, "SUBSCRIBER2"), 
            daemon=True
        )
        
        listener1.start()
        listener2.start()
        
        # Keep subscribers alive for the demo
        time.sleep(5)
        
        print("[SUBSCRIBER1] 🔄 Unsubscribing from topics...")
        client1.unsubscribe("news/tech")
        client1.unsubscribe("news/sports")
        
        print("[SUBSCRIBER2] 🔄 Unsubscribing from topics...")
        client2.unsubscribe("alerts/system")
        client2.unsubscribe("data/sensors") 
        client2.unsubscribe("events/user")
        
    except ConnectionRefusedError:
        print("[SUBSCRIBER] ❌ Could not connect to server. Is it running?")
    except Exception as e:
        print(f"[SUBSCRIBER] ❌ Error: {e}")
    finally:
        try:
            client1.close()
            client2.close()
            print("[SUBSCRIBER] 🔒 Connections closed")
        except:
            pass

def main():
    """Run the complete PubSub demonstration."""
    print("=" * 60)
    print("🎯 kn-sock PubSub Complete Working Example")
    print("=" * 60)
    print()
    
    try:
        # Start server in background
        print("1️⃣  Starting PubSub Server...")
        server_thread = threading.Thread(target=start_pubsub_server_demo, daemon=True)
        server_thread.start()
        time.sleep(2)  # Give server time to start
        
        # Start subscribers in background
        print("2️⃣  Starting Subscriber Clients...")
        subscriber_thread = threading.Thread(target=subscriber_demo, daemon=True)
        subscriber_thread.start()
        time.sleep(1)  # Give subscribers time to connect
        
        # Start publisher
        print("3️⃣  Starting Publisher Client...")
        publisher_demo()
        
        # Wait for messages to be processed
        print("\n4️⃣  Waiting for message processing...")
        time.sleep(3)
        
        print("\n" + "=" * 60)
        print("✅ PubSub Example Completed Successfully!")
        print("=" * 60)
        
        print("\n💡 What happened:")
        print("   • PubSub server started on port 8080")
        print("   • Two subscriber clients connected to different topics")
        print("   • Publisher sent 5 different messages")
        print("   • Subscribers received messages based on their subscriptions")
        print("   • Server logged all activities with custom handler")
        
        print("\n🔧 Try this yourself:")
        print("   1. Copy this example to a new file")
        print("   2. Run: python your_file.py")
        print("   3. Experiment with different topics and messages")
        
        print("\n🌐 Server is still running in background...")
        print("   You can connect with: kn-sock pubsub-client localhost 8080 test 'Hello'")
        
    except KeyboardInterrupt:
        print("\n🛑 Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running example: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
