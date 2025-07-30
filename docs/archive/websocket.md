# WebSocket Utilities

kn-sock provides CLI and Python APIs for real-time WebSocket communication for chat, real-time dashboards, or browser-to-server data flows.

## CLI Commands

### 1. Start a WebSocket Echo Server

Launch a WebSocket server that listens for incoming connections and echoes any messages received.

| Command                                   | Description                   |
|--------------------------------------------|-------------------------------|
| `run-websocket-server <port>`              | Start WebSocket echo server   |

**Example:**
```sh
docker-compose run --rm knsock run-websocket-server 9000
# Or: knsock run-websocket-server 9000
```
**Output:**
```
[WebSocket][SERVER] Listening on 0.0.0.0:9000
```

### 2. WebSocket Client

Connect to a WebSocket server, send a message, and display the server’s response.

| Command                                       | Description                   |
|-----------------------------------------------|-------------------------------|
| `websocket-client <host> <port> <message>`    | Connect/send/receive via WebSocket |

**Example:**
```sh
docker-compose run --rm knsock websocket-client 172.18.0.2 9000 "Hello WebSocket"
```
**Output:**
```
[WebSocket][CLIENT] Connected to ws://172.18.0.2:9000
[WebSocket][CLIENT] Sent: Hello WebSocket
[WebSocket][CLIENT] Received: Echo: Hello WebSocket
```

#### Options Table
| Option        | Description                           |
|---------------|---------------------------------------|
| `<port>`      | Port number for server/client         |
| `<host>`      | IP or hostname of server             |
| `<message>`   | Message to send (client only)        |

## Python API

### Start a WebSocket Server
```python
from kn_sock import start_websocket_server

def echo_handler(ws, addr):
    for msg in ws:
        print(f"Received: {msg}")
        ws.send("Echo: " + msg)

start_websocket_server(9000, echo_handler)
```

### Connect as WebSocket Client
```python
from kn_sock import connect_websocket

ws = connect_websocket('127.0.0.1', 9000)
ws.send("Hello WebSocket")
response = ws.recv()
print(response)
ws.close()
```

### Sample Output
**Server terminal:**
```
[WebSocket][SERVER] Listening on 0.0.0.0:9000
[WebSocket][SERVER] Connection from ('172.18.0.1', 33512)
[WebSocket][SERVER] Received: Hello WebSocket
```

**Client terminal:**
```
[WebSocket][CLIENT] Connected to ws://172.18.0.2:9000
[WebSocket][CLIENT] Sent: Hello WebSocket
[WebSocket][CLIENT] Received: Echo: Hello WebSocket
```

## Known Issues & Troubleshooting
| Issue                        | Symptom/Output                              | Solution                                           |
|------------------------------|---------------------------------------------|----------------------------------------------------|
| Port already in use          | `[Errno 98] Address already in use`         | Use a different port or kill existing process      |
| Connection refused           | `ConnectionRefusedError`                    | Start the server before connecting                 |
| Hostname not found           | `[Errno -2] Name or service not known`      | Use container IP, not name, in Docker setups       |
| Browser client can't connect | No handshake or failed connection           | Ensure proper port, firewall, and server up        |

## Testing
### Manual Test
Start the WebSocket server:
```sh
docker-compose run --rm knsock run-websocket-server 9000
```

In another terminal:
```sh
docker-compose run --rm knsock websocket-client <server-ip> 9000 "Hello WebSocket"
# Example: websocket-client 172.18.0.2 9000 "Hello WebSocket"
```

Confirm that the client receives `Echo: Hello WebSocket`.