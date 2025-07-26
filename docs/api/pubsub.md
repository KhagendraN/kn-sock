# Pub/Sub Messaging Utilities

kn-sock offers simple publish/subscribe (pub/sub) messaging for distributed notification and event-driven testing.
  
Use pub/sub for broadcasting updates, fan-out, or basic topic-based communication.

## CLI Commands

### 1. Start a Pub/Sub Server

Launch a pub/sub server that handles topic subscriptions and message publishing.

| Command                                  | Description                      |
|-------------------------------------------|----------------------------------|
| `run-pubsub-server <port>`                | Start a pub/sub messaging server |

**Example:**
```sh
docker-compose run --rm knsock run-pubsub-server 9100
# Or: knsock run-pubsub-server 9100
```
**Output:**
```
[PUBSUB][SERVER] Listening on 0.0.0.0:9100
```

### 2. Connect as a Pub/Sub Client

Subscribe to a topic, publish messages, and receive updates.

| Command                                  | Description                   |
|-------------------------------------------|-------------------------------|
| `pubsub-client <host> <port>`            | Connect as pub/sub client     |

**Example:**
```sh
docker-compose run --rm knsock pubsub-client 172.18.0.2 9100
```
Interactive client: enter commands in the terminal, e.g.:
```bash
subscribe test
publish test Hello, PubSub!
# Output: Received on [test]: Hello, PubSub!
```

#### Options Table
| Option        | Description                           |
|---------------|---------------------------------------|
| `<port>`      | Port for server/client               |
| `<host>`      | IP/hostname of server (client only)  |

## Python API

### Start a Pub/Sub Server
```python
from kn_sock import start_pubsub_server

start_pubsub_server(9100)
```

### Connect as a Pub/Sub Client
```python
from kn_sock import PubSubClient

client = PubSubClient('127.0.0.1', 9100)
client.subscribe('test')
client.publish('test', 'Hello, PubSub!')
# Listen for messages...
```

### Sample Output
**Server terminal:**
```
[PUBSUB][SERVER] Listening on 0.0.0.0:9100
[PUBSUB][SERVER] Client subscribed to: test
[PUBSUB][SERVER] Message published to [test]: Hello, PubSub!
```

**Client terminal:**
```
[PUBSUB][CLIENT] Subscribed to topic: test
[PUBSUB][CLIENT] Published to topic [test]: Hello, PubSub!
[PUBSUB][CLIENT] Received on [test]: Hello, PubSub!
```

## Known Issues & Troubleshooting
| Issue                        | Symptom/Output                              | Solution                                           |
|------------------------------|---------------------------------------------|----------------------------------------------------|
| No messages received         | No output after subscribe                   | Make sure at least one message published           |
| Connection refused           | `ConnectionRefusedError`                    | Ensure server is running                           |
| Hostname not found           | `[Errno -2] Name or service not known`      | Use container IP in Docker                         |

## Testing
### Manual Test
Start the pub/sub server:
```sh
docker-compose run --rm knsock run-pubsub-server 9100
```

In another terminal, connect as a client:
```sh
docker-compose run --rm knsock pubsub-client <server-ip> 9100
# Example: pubsub-client 172.18.0.2 9100
```

In the client, type:
```bash
subscribe test
publish test Hello, PubSub!
```

You should see the published message received in the client output.