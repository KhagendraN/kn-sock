# Publish/Subscribe Messaging

kn-sock provides a robust publish/subscribe (pub/sub) messaging system for decoupled, scalable communication between applications.

## Overview

Pub/Sub features in kn-sock:
- **Topic-based messaging**: Organize messages by topics
- **Multiple subscribers**: Many clients can subscribe to the same topic
- **Message persistence**: Optional message persistence and replay
- **Quality of Service**: Configurable delivery guarantees
- **Broker architecture**: Centralized message distribution
- **Pattern matching**: Subscribe to topics using wildcards
- **Message filtering**: Server-side message filtering capabilities

## Basic Pub/Sub Usage

### Starting a Pub/Sub Broker

```python
from kn_sock import start_pubsub_broker

def message_handler(topic, message, publisher_info):
    """
    Handle published messages (optional custom processing).
    
    Args:
        topic (str): The topic the message was published to
        message (str): The message content
        publisher_info (dict): Information about the publisher
    """
    print(f"Message on topic '{topic}': {message}")
    print(f"Published by: {publisher_info}")

# Start the pub/sub broker
start_pubsub_broker(
    port=8080,
    host='0.0.0.0',
    message_handler=message_handler,  # Optional
    persistence=True,  # Enable message persistence
    max_messages=1000  # Maximum messages to store per topic
)
```

### Publisher Client

```python
from kn_sock import PubSubPublisher

def publisher_example():
    """Example publisher client."""
    
    # Connect to the broker
    publisher = PubSubPublisher("localhost", 8080)
    
    try:
        # Publish messages to different topics
        publisher.publish("news/technology", "New AI breakthrough announced!")
        publisher.publish("news/sports", "Championship game tonight")
        publisher.publish("alerts/system", "Server maintenance scheduled")
        
        # Publish with metadata
        publisher.publish(
            "user/updates", 
            "User profile updated",
            metadata={
                "user_id": "12345",
                "timestamp": "2024-01-15T10:30:00Z",
                "priority": "normal"
            }
        )
        
        # Publish JSON data
        import json
        data = {
            "event": "order_created",
            "order_id": "ORD-789",
            "amount": 99.99,
            "customer": "john@example.com"
        }
        publisher.publish("orders/created", json.dumps(data))
        
    finally:
        publisher.disconnect()

publisher_example()
```

### Subscriber Client

```python
from kn_sock import PubSubSubscriber
import threading

def subscriber_example():
    """Example subscriber client."""
    
    # Connect to the broker
    subscriber = PubSubSubscriber("localhost", 8080)
    
    def handle_news_message(topic, message, metadata=None):
        """Handle news messages."""
        print(f"NEWS: [{topic}] {message}")
        if metadata:
            print(f"Metadata: {metadata}")
    
    def handle_alert_message(topic, message, metadata=None):
        """Handle alert messages."""
        print(f"ALERT: [{topic}] {message}")
        # Could trigger notifications, emails, etc.
    
    def handle_order_message(topic, message, metadata=None):
        """Handle order messages."""
        import json
        try:
            order_data = json.loads(message)
            print(f"ORDER: {order_data['event']} - ID: {order_data['order_id']}")
        except json.JSONDecodeError:
            print(f"ORDER: [{topic}] {message}")
    
    try:
        # Subscribe to specific topics
        subscriber.subscribe("news/technology", handle_news_message)
        subscriber.subscribe("news/sports", handle_news_message)
        subscriber.subscribe("alerts/system", handle_alert_message)
        subscriber.subscribe("orders/created", handle_order_message)
        
        # Subscribe with wildcards
        subscriber.subscribe("user/*", lambda t, m, meta: print(f"USER EVENT: [{t}] {m}"))
        
        # Start listening for messages
        print("Subscriber started. Press Ctrl+C to stop.")
        subscriber.start_listening()
        
    except KeyboardInterrupt:
        print("\nShutting down subscriber...")
    finally:
        subscriber.disconnect()

subscriber_example()
```

## Advanced Pub/Sub Features

### Message Persistence and Replay

```python
from kn_sock import PubSubBroker, PubSubSubscriber

class PersistentPubSubBroker(PubSubBroker):
    """Pub/Sub broker with advanced persistence features."""
    
    def __init__(self, port, host='0.0.0.0'):
        super().__init__(port, host)
        self.message_history = {}  # topic -> list of messages
        self.max_history_per_topic = 100
        
    def publish_message(self, topic, message, publisher_info, metadata=None):
        """Publish message with persistence."""
        
        # Store message in history
        if topic not in self.message_history:
            self.message_history[topic] = []
        
        message_entry = {
            "message": message,
            "publisher": publisher_info,
            "metadata": metadata,
            "timestamp": time.time()
        }
        
        self.message_history[topic].append(message_entry)
        
        # Limit history size
        if len(self.message_history[topic]) > self.max_history_per_topic:
            self.message_history[topic].pop(0)
        
        # Call parent to distribute message
        super().publish_message(topic, message, publisher_info, metadata)
    
    def replay_messages(self, topic, subscriber_info, since_timestamp=None):
        """Replay historical messages to a subscriber."""
        
        if topic not in self.message_history:
            return
        
        for entry in self.message_history[topic]:
            if since_timestamp is None or entry["timestamp"] >= since_timestamp:
                self.send_to_subscriber(subscriber_info, topic, entry)
    
    def get_topic_stats(self, topic):
        """Get statistics for a topic."""
        if topic not in self.message_history:
            return {"message_count": 0, "subscribers": 0}
        
        return {
            "message_count": len(self.message_history[topic]),
            "subscribers": len(self.get_subscribers(topic)),
            "latest_message": self.message_history[topic][-1] if self.message_history[topic] else None
        }

# Usage with replay functionality
def subscriber_with_replay():
    """Subscriber that requests message replay."""
    
    subscriber = PubSubSubscriber("localhost", 8080)
    
    def message_handler(topic, message, metadata=None):
        print(f"Received: [{topic}] {message}")
    
    # Subscribe and request replay of last hour's messages
    import time
    one_hour_ago = time.time() - 3600
    
    subscriber.subscribe("news/*", message_handler)
    subscriber.request_replay("news/*", since_timestamp=one_hour_ago)
    
    subscriber.start_listening()
```

### Quality of Service (QoS) Levels

```python
from kn_sock import PubSubPublisher, PubSubSubscriber
from enum import Enum

class QoSLevel(Enum):
    """Quality of Service levels."""
    AT_MOST_ONCE = 0   # Fire and forget
    AT_LEAST_ONCE = 1  # Guaranteed delivery, possible duplicates
    EXACTLY_ONCE = 2   # Guaranteed delivery, no duplicates

class QoSPubSubPublisher(PubSubPublisher):
    """Publisher with QoS support."""
    
    def __init__(self, host, port):
        super().__init__(host, port)
        self.message_acknowledgments = {}
        self.message_counter = 0
    
    def publish_with_qos(self, topic, message, qos_level=QoSLevel.AT_MOST_ONCE, timeout=30):
        """Publish message with specified QoS level."""
        
        if qos_level == QoSLevel.AT_MOST_ONCE:
            # Simple fire-and-forget
            return self.publish(topic, message)
        
        elif qos_level == QoSLevel.AT_LEAST_ONCE:
            # Wait for acknowledgment, retry if needed
            message_id = self.generate_message_id()
            
            for attempt in range(3):  # Max 3 attempts
                self.publish(topic, message, metadata={"message_id": message_id, "qos": 1})
                
                if self.wait_for_ack(message_id, timeout):
                    return True
                
                print(f"Retry {attempt + 1} for message {message_id}")
            
            return False
        
        elif qos_level == QoSLevel.EXACTLY_ONCE:
            # Two-phase commit for exactly-once delivery
            return self.publish_exactly_once(topic, message, timeout)
    
    def generate_message_id(self):
        """Generate unique message ID."""
        self.message_counter += 1
        return f"{self.client_id}_{self.message_counter}"
    
    def wait_for_ack(self, message_id, timeout):
        """Wait for message acknowledgment."""
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if message_id in self.message_acknowledgments:
                del self.message_acknowledgments[message_id]
                return True
            time.sleep(0.1)
        
        return False
    
    def handle_acknowledgment(self, ack_data):
        """Handle acknowledgment from broker."""
        message_id = ack_data.get("message_id")
        if message_id:
            self.message_acknowledgments[message_id] = True

# QoS Subscriber with acknowledgments
class QoSPubSubSubscriber(PubSubSubscriber):
    """Subscriber with QoS acknowledgment support."""
    
    def __init__(self, host, port):
        super().__init__(host, port)
        self.processed_messages = set()  # For exactly-once processing
    
    def handle_qos_message(self, topic, message, metadata=None):
        """Handle message with QoS processing."""
        
        qos_level = metadata.get("qos", 0) if metadata else 0
        message_id = metadata.get("message_id") if metadata else None
        
        if qos_level == 1 and message_id:
            # Send acknowledgment for at-least-once
            self.send_acknowledgment(message_id)
        
        elif qos_level == 2 and message_id:
            # Handle exactly-once processing
            if message_id in self.processed_messages:
                print(f"Duplicate message {message_id} ignored")
                return
            
            self.processed_messages.add(message_id)
            self.send_acknowledgment(message_id)
        
        # Process the message
        self.process_message(topic, message, metadata)
    
    def send_acknowledgment(self, message_id):
        """Send acknowledgment to broker."""
        ack_data = {
            "type": "acknowledgment",
            "message_id": message_id
        }
        self.send_control_message(ack_data)
    
    def process_message(self, topic, message, metadata):
        """Process the actual message (override in subclass)."""
        print(f"Processing: [{topic}] {message}")

# Usage example
publisher = QoSPubSubPublisher("localhost", 8080)

# Publish with different QoS levels
publisher.publish_with_qos("critical/alerts", "System failure!", QoSLevel.EXACTLY_ONCE)
publisher.publish_with_qos("notifications", "New message", QoSLevel.AT_LEAST_ONCE)
publisher.publish_with_qos("metrics", "CPU: 45%", QoSLevel.AT_MOST_ONCE)
```

### Topic Hierarchies and Wildcards

```python
from kn_sock import PubSubSubscriber

def wildcard_subscription_example():
    """Example of wildcard topic subscriptions."""
    
    subscriber = PubSubSubscriber("localhost", 8080)
    
    def sports_handler(topic, message, metadata=None):
        """Handle all sports-related messages."""
        sport = topic.split('/')[-1]  # Extract sport from topic
        print(f"SPORTS [{sport.upper()}]: {message}")
    
    def alert_handler(topic, message, metadata=None):
        """Handle all alert messages."""
        alert_level = topic.split('/')[-1]
        print(f"ALERT [{alert_level.upper()}]: {message}")
    
    def user_activity_handler(topic, message, metadata=None):
        """Handle user activity messages."""
        user_id = topic.split('/')[1]  # Extract user ID
        action = topic.split('/')[-1]
        print(f"User {user_id} performed action: {action}")
    
    # Subscribe to topic hierarchies
    subscriber.subscribe("sports/*", sports_handler)           # sports/football, sports/basketball
    subscriber.subscribe("alerts/*", alert_handler)           # alerts/critical, alerts/warning
    subscriber.subscribe("user/*/activity", user_activity_handler)  # user/123/activity, user/456/activity
    
    # Multi-level wildcards
    subscriber.subscribe("system/*/logs/*", lambda t, m, meta: print(f"LOG: {t} -> {m}"))
    
    # Exact topic subscription
    subscriber.subscribe("admin/shutdown", lambda t, m, meta: print(f"SHUTDOWN: {m}"))
    
    subscriber.start_listening()

# Publisher with hierarchical topics
def hierarchical_publisher_example():
    """Example of publishing to hierarchical topics."""
    
    from kn_sock import PubSubPublisher
    
    publisher = PubSubPublisher("localhost", 8080)
    
    # Sports topics
    publisher.publish("sports/football", "Goal scored!")
    publisher.publish("sports/basketball", "Three-pointer!")
    publisher.publish("sports/tennis", "Match point!")
    
    # Alert topics
    publisher.publish("alerts/critical", "Database connection lost")
    publisher.publish("alerts/warning", "High memory usage detected")
    publisher.publish("alerts/info", "Backup completed successfully")
    
    # User activity topics
    publisher.publish("user/123/activity", "logged_in")
    publisher.publish("user/456/activity", "file_uploaded")
    publisher.publish("user/789/activity", "password_changed")
    
    # System logs
    publisher.publish("system/web/logs/access", "GET /api/users 200")
    publisher.publish("system/db/logs/query", "SELECT * FROM users executed")
    
    publisher.disconnect()
```

### Message Filtering

```python
from kn_sock import PubSubBroker

class FilteringPubSubBroker(PubSubBroker):
    """Pub/Sub broker with server-side message filtering."""
    
    def __init__(self, port, host='0.0.0.0'):
        super().__init__(port, host)
        self.subscriber_filters = {}  # subscriber_id -> filters
    
    def add_subscriber_filter(self, subscriber_id, filter_func):
        """Add a filter function for a subscriber."""
        if subscriber_id not in self.subscriber_filters:
            self.subscriber_filters[subscriber_id] = []
        self.subscriber_filters[subscriber_id].append(filter_func)
    
    def should_deliver_message(self, subscriber_id, topic, message, metadata):
        """Check if message should be delivered to subscriber."""
        
        if subscriber_id not in self.subscriber_filters:
            return True  # No filters, deliver all messages
        
        for filter_func in self.subscriber_filters[subscriber_id]:
            if not filter_func(topic, message, metadata):
                return False
        
        return True
    
    def distribute_message(self, topic, message, metadata=None):
        """Distribute message to filtered subscribers."""
        
        for subscriber_id, subscriber_info in self.get_topic_subscribers(topic).items():
            if self.should_deliver_message(subscriber_id, topic, message, metadata):
                self.send_to_subscriber(subscriber_info, topic, message, metadata)

# Filter functions
def priority_filter(min_priority):
    """Create a filter for minimum priority messages."""
    def filter_func(topic, message, metadata):
        if not metadata or 'priority' not in metadata:
            return True  # No priority info, allow message
        
        priority_levels = {'low': 1, 'normal': 2, 'high': 3, 'critical': 4}
        message_priority = priority_levels.get(metadata['priority'], 0)
        required_priority = priority_levels.get(min_priority, 0)
        
        return message_priority >= required_priority
    
    return filter_func

def content_filter(keywords):
    """Create a filter for messages containing specific keywords."""
    def filter_func(topic, message, metadata):
        message_lower = message.lower()
        return any(keyword.lower() in message_lower for keyword in keywords)
    
    return filter_func

def time_filter(start_hour, end_hour):
    """Create a filter for messages within specific hours."""
    def filter_func(topic, message, metadata):
        import datetime
        current_hour = datetime.datetime.now().hour
        return start_hour <= current_hour <= end_hour
    
    return filter_func

# Usage example
def filtered_subscriber_example():
    """Example subscriber with server-side filtering."""
    
    from kn_sock import PubSubSubscriber
    
    subscriber = PubSubSubscriber("localhost", 8080)
    
    # Register filters with the broker
    subscriber.add_filter(priority_filter('high'))  # Only high/critical priority
    subscriber.add_filter(content_filter(['urgent', 'error', 'failure']))  # Only urgent content
    subscriber.add_filter(time_filter(9, 17))  # Only during business hours
    
    def filtered_handler(topic, message, metadata=None):
        print(f"FILTERED MESSAGE: [{topic}] {message}")
        if metadata:
            print(f"Priority: {metadata.get('priority', 'unknown')}")
    
    subscriber.subscribe("alerts/*", filtered_handler)
    subscriber.start_listening()
```

## Pub/Sub Patterns

### Request-Reply Pattern

```python
from kn_sock import PubSubPublisher, PubSubSubscriber
import uuid
import threading
import time

class RequestReplyClient:
    """Client that implements request-reply pattern over pub/sub."""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_id = str(uuid.uuid4())
        self.publisher = PubSubPublisher(host, port)
        self.subscriber = PubSubSubscriber(host, port)
        self.pending_requests = {}
        self.reply_topic = f"replies/{self.client_id}"
        
        # Subscribe to reply topic
        self.subscriber.subscribe(self.reply_topic, self.handle_reply)
        
        # Start subscriber in background
        self.subscriber_thread = threading.Thread(
            target=self.subscriber.start_listening, 
            daemon=True
        )
        self.subscriber_thread.start()
    
    def send_request(self, service_topic, request_data, timeout=30):
        """Send request and wait for reply."""
        
        request_id = str(uuid.uuid4())
        
        # Prepare request message
        request_message = {
            "id": request_id,
            "reply_to": self.reply_topic,
            "data": request_data,
            "timestamp": time.time()
        }
        
        # Create event to wait for reply
        reply_event = threading.Event()
        self.pending_requests[request_id] = {
            "event": reply_event,
            "reply": None
        }
        
        try:
            # Send request
            self.publisher.publish(
                service_topic, 
                json.dumps(request_message)
            )
            
            # Wait for reply
            if reply_event.wait(timeout):
                return self.pending_requests[request_id]["reply"]
            else:
                raise TimeoutError(f"Request {request_id} timed out")
        
        finally:
            # Clean up
            if request_id in self.pending_requests:
                del self.pending_requests[request_id]
    
    def handle_reply(self, topic, message, metadata=None):
        """Handle reply message."""
        try:
            reply_data = json.loads(message)
            request_id = reply_data.get("request_id")
            
            if request_id in self.pending_requests:
                self.pending_requests[request_id]["reply"] = reply_data
                self.pending_requests[request_id]["event"].set()
        
        except json.JSONDecodeError:
            print(f"Invalid reply format: {message}")

class RequestReplyService:
    """Service that handles requests and sends replies."""
    
    def __init__(self, host, port, service_name):
        self.host = host
        self.port = port
        self.service_name = service_name
        self.publisher = PubSubPublisher(host, port)
        self.subscriber = PubSubSubscriber(host, port)
        
        # Subscribe to service topic
        service_topic = f"services/{service_name}"
        self.subscriber.subscribe(service_topic, self.handle_request)
    
    def handle_request(self, topic, message, metadata=None):
        """Handle incoming request."""
        try:
            request_data = json.loads(message)
            request_id = request_data.get("id")
            reply_topic = request_data.get("reply_to")
            data = request_data.get("data")
            
            # Process the request
            reply_data = self.process_request(data)
            
            # Send reply
            reply_message = {
                "request_id": request_id,
                "data": reply_data,
                "timestamp": time.time(),
                "service": self.service_name
            }
            
            self.publisher.publish(reply_topic, json.dumps(reply_message))
        
        except Exception as e:
            print(f"Error handling request: {e}")
    
    def process_request(self, data):
        """Process request data (override in subclass)."""
        # Example: echo service
        return f"Echo: {data}"
    
    def start(self):
        """Start the service."""
        print(f"Service {self.service_name} started")
        self.subscriber.start_listening()

# Usage example
import json

# Start a calculator service
class CalculatorService(RequestReplyService):
    """Calculator service example."""
    
    def process_request(self, data):
        """Process calculation request."""
        try:
            operation = data.get("operation")
            operands = data.get("operands", [])
            
            if operation == "add":
                result = sum(operands)
            elif operation == "multiply":
                result = 1
                for operand in operands:
                    result *= operand
            elif operation == "divide":
                result = operands[0] / operands[1] if len(operands) >= 2 else None
            else:
                result = f"Unknown operation: {operation}"
            
            return {"result": result, "status": "success"}
        
        except Exception as e:
            return {"error": str(e), "status": "error"}

# Start calculator service
calc_service = CalculatorService("localhost", 8080, "calculator")
service_thread = threading.Thread(target=calc_service.start, daemon=True)
service_thread.start()

# Use the service
client = RequestReplyClient("localhost", 8080)

# Send calculation requests
add_result = client.send_request(
    "services/calculator",
    {"operation": "add", "operands": [10, 20, 30]}
)
print(f"Addition result: {add_result}")

multiply_result = client.send_request(
    "services/calculator", 
    {"operation": "multiply", "operands": [5, 6]}
)
print(f"Multiplication result: {multiply_result}")
```

## Performance and Scaling

### Clustered Pub/Sub Brokers

```python
from kn_sock import PubSubBroker
import threading
import json

class ClusteredPubSubBroker(PubSubBroker):
    """Pub/Sub broker with clustering support."""
    
    def __init__(self, port, host='0.0.0.0', cluster_nodes=None):
        super().__init__(port, host)
        self.cluster_nodes = cluster_nodes or []
        self.broker_id = f"{host}:{port}"
        self.cluster_connections = {}
        
        # Connect to other brokers in cluster
        self.connect_to_cluster()
    
    def connect_to_cluster(self):
        """Connect to other brokers in the cluster."""
        for node in self.cluster_nodes:
            if node != self.broker_id:
                try:
                    connection = self.create_cluster_connection(node)
                    self.cluster_connections[node] = connection
                    print(f"Connected to cluster node: {node}")
                except Exception as e:
                    print(f"Failed to connect to cluster node {node}: {e}")
    
    def publish_to_cluster(self, topic, message, metadata=None, origin_broker=None):
        """Publish message to cluster nodes."""
        
        # Don't forward if we're the origin
        if origin_broker == self.broker_id:
            return
        
        cluster_message = {
            "type": "cluster_publish",
            "topic": topic,
            "message": message,
            "metadata": metadata,
            "origin_broker": self.broker_id
        }
        
        for node_id, connection in self.cluster_connections.items():
            try:
                connection.send(json.dumps(cluster_message))
            except Exception as e:
                print(f"Failed to forward to cluster node {node_id}: {e}")
    
    def handle_cluster_message(self, cluster_message):
        """Handle message from cluster node."""
        message_type = cluster_message.get("type")
        
        if message_type == "cluster_publish":
            # Distribute to local subscribers only
            self.distribute_locally(
                cluster_message["topic"],
                cluster_message["message"],
                cluster_message.get("metadata"),
                cluster_message.get("origin_broker")
            )
    
    def publish_message(self, topic, message, publisher_info, metadata=None):
        """Publish message locally and to cluster."""
        
        # Distribute locally
        super().publish_message(topic, message, publisher_info, metadata)
        
        # Forward to cluster
        self.publish_to_cluster(topic, message, metadata)

# Load balancing subscriber connections
class LoadBalancedSubscriber:
    """Subscriber that connects to multiple brokers for load balancing."""
    
    def __init__(self, broker_addresses):
        self.broker_addresses = broker_addresses
        self.subscribers = []
        self.current_broker = 0
        
        # Create connections to all brokers
        for address in broker_addresses:
            host, port = address.split(':')
            subscriber = PubSubSubscriber(host, int(port))
            self.subscribers.append(subscriber)
    
    def subscribe(self, topic, handler):
        """Subscribe to topic on next available broker."""
        broker = self.subscribers[self.current_broker]
        broker.subscribe(topic, handler)
        
        # Round-robin to next broker
        self.current_broker = (self.current_broker + 1) % len(self.subscribers)
    
    def start_all(self):
        """Start all subscriber connections."""
        threads = []
        for subscriber in self.subscribers:
            thread = threading.Thread(target=subscriber.start_listening, daemon=True)
            thread.start()
            threads.append(thread)
        return threads

# Usage example
cluster_nodes = ["localhost:8080", "localhost:8081", "localhost:8082"]

# Start clustered brokers
brokers = []
for i, node in enumerate(cluster_nodes):
    host, port = node.split(':')
    other_nodes = [n for n in cluster_nodes if n != node]
    
    broker = ClusteredPubSubBroker(int(port), host, other_nodes)
    brokers.append(broker)
    
    # Start each broker in a separate thread
    broker_thread = threading.Thread(target=broker.start, daemon=True)
    broker_thread.start()

# Use load-balanced subscriber
load_balanced_subscriber = LoadBalancedSubscriber(cluster_nodes)
load_balanced_subscriber.subscribe("test/*", lambda t, m, meta: print(f"Received: {t} -> {m}"))
load_balanced_subscriber.start_all()
```

## Monitoring and Metrics

```python
import time
import threading
from collections import defaultdict, deque

class MonitoredPubSubBroker(PubSubBroker):
    """Pub/Sub broker with monitoring and metrics."""
    
    def __init__(self, port, host='0.0.0.0'):
        super().__init__(port, host)
        
        # Metrics storage
        self.metrics = {
            "messages_published": 0,
            "messages_delivered": 0,
            "active_subscribers": 0,
            "topics_count": 0,
            "uptime_start": time.time()
        }
        
        self.topic_metrics = defaultdict(lambda: {
            "message_count": 0,
            "subscriber_count": 0,
            "last_message_time": None
        })
        
        self.performance_history = deque(maxlen=100)  # Last 100 measurements
        
        # Start metrics collection thread
        self.metrics_thread = threading.Thread(target=self.collect_metrics, daemon=True)
        self.metrics_thread.start()
    
    def publish_message(self, topic, message, publisher_info, metadata=None):
        """Publish message with metrics tracking."""
        start_time = time.time()
        
        # Call parent method
        super().publish_message(topic, message, publisher_info, metadata)
        
        # Update metrics
        self.metrics["messages_published"] += 1
        self.topic_metrics[topic]["message_count"] += 1
        self.topic_metrics[topic]["last_message_time"] = time.time()
        
        # Track performance
        end_time = time.time()
        self.performance_history.append({
            "publish_time": end_time - start_time,
            "timestamp": end_time,
            "topic": topic
        })
    
    def add_subscriber(self, topic, subscriber_info):
        """Add subscriber with metrics tracking."""
        super().add_subscriber(topic, subscriber_info)
        
        self.metrics["active_subscribers"] += 1
        self.topic_metrics[topic]["subscriber_count"] += 1
        self.metrics["topics_count"] = len(self.topic_metrics)
    
    def remove_subscriber(self, topic, subscriber_id):
        """Remove subscriber with metrics tracking."""
        super().remove_subscriber(topic, subscriber_id)
        
        self.metrics["active_subscribers"] -= 1
        if topic in self.topic_metrics:
            self.topic_metrics[topic]["subscriber_count"] -= 1
    
    def collect_metrics(self):
        """Collect performance metrics periodically."""
        while True:
            time.sleep(10)  # Collect every 10 seconds
            
            # Calculate average publish time
            if self.performance_history:
                recent_times = [entry["publish_time"] for entry in self.performance_history]
                avg_publish_time = sum(recent_times) / len(recent_times)
                self.metrics["avg_publish_time_ms"] = avg_publish_time * 1000
            
            # Calculate uptime
            self.metrics["uptime_seconds"] = time.time() - self.metrics["uptime_start"]
            
            # Log metrics (or send to monitoring system)
            self.log_metrics()
    
    def log_metrics(self):
        """Log current metrics."""
        print(f"Pub/Sub Metrics:")
        print(f"  Messages Published: {self.metrics['messages_published']}")
        print(f"  Active Subscribers: {self.metrics['active_subscribers']}")
        print(f"  Topics: {self.metrics['topics_count']}")
        print(f"  Uptime: {self.metrics['uptime_seconds']:.1f}s")
        if "avg_publish_time_ms" in self.metrics:
            print(f"  Avg Publish Time: {self.metrics['avg_publish_time_ms']:.2f}ms")
        print()
    
    def get_metrics(self):
        """Get current metrics."""
        return {
            "broker_metrics": self.metrics.copy(),
            "topic_metrics": dict(self.topic_metrics),
            "performance_history": list(self.performance_history)
        }
    
    def get_health_status(self):
        """Get broker health status."""
        health = {
            "status": "healthy",
            "checks": {
                "uptime": self.metrics["uptime_seconds"] > 0,
                "subscribers": self.metrics["active_subscribers"] >= 0,
                "performance": True
            }
        }
        
        # Check performance
        if "avg_publish_time_ms" in self.metrics:
            if self.metrics["avg_publish_time_ms"] > 100:  # >100ms is concerning
                health["checks"]["performance"] = False
                health["status"] = "degraded"
        
        return health

# Usage with monitoring
broker = MonitoredPubSubBroker(8080)

# Start broker in background
broker_thread = threading.Thread(target=broker.start, daemon=True)
broker_thread.start()

# Monitor health periodically
def health_monitor():
    while True:
        time.sleep(30)
        health = broker.get_health_status()
        print(f"Broker Health: {health['status']}")
        
        if health["status"] != "healthy":
            print(f"Health issues detected: {health}")

health_thread = threading.Thread(target=health_monitor, daemon=True)
health_thread.start()
```

## See Also

- **[TCP Protocol](tcp.md)** - For reliable message transport
- **[JSON Communication](json.md)** - For structured message data
- **[WebSocket Protocol](websocket.md)** - For real-time communication
- **[RPC](rpc.md)** - For remote procedure calls
- **[Examples](../examples.md)** - Pub/Sub application examples
