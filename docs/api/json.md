# JSON Messaging Utilities

kn-sock supports sending and receiving structured JSON data over sockets, making it easy to build APIs, automation tools, and structured communication between systems.

## CLI Commands

### 1. JSON over TCP/UDP

While there are no dedicated `send-json` or `run-json-server` CLI commands, you can send JSON strings as messages using the standard TCP/UDP commands.  
JSON socket helpers in the Python API handle encoding/decoding for you.

**Example:**
```sh
docker-compose run --rm knsock send-tcp 172.18.0.2 8080 '{"type": "ping", "payload": 123}'
```

## Python API

### Send and Receive JSON Messages (TCP Example)
```python
from kn_sock.json_socket import send_json, start_json_server

def handle_json(data, addr, conn):
    print(f"Received JSON: {data}")
    conn.sendall({"type": "pong", "payload": 456})

# Start a TCP JSON echo server on port 7000
start_json_server(7000, handle_json)
```

### Send a JSON message (client):
```python
from kn_sock.json_socket import send_json

response = send_json("127.0.0.1", 7000, {"type": "ping", "payload": 123})
print(response)
```

#### Options Table
| Option        | Description                           |
|---------------|---------------------------------------|
| `<host>`      | Server IP or hostname                 |
| `<port>`      | Port number                           |
| `<json>`      | JSON string or dict to send           |

## Sample Output
**Server terminal:**
```
[JSON][SERVER] Received from ('172.18.0.1', 56601): {'type': 'ping', 'payload': 123}
```

**Client terminal:**
```
[JSON][CLIENT] Sent: {'type': 'ping', 'payload': 123}
[JSON][CLIENT] Received: {'type': 'pong', 'payload': 456}
```

## Known Issues & Troubleshooting
| Issue                        | Symptom/Output                              | Solution                                           |
|------------------------------|---------------------------------------------|----------------------------------------------------|
| Invalid JSON                 | Exception or parse error                    | Validate JSON syntax before sending                |
| No response                  | Hangs or empty result                       | Check server is running and handles JSON           |
| Encoding errors              | Unicode/byte issues                         | Always use UTF-8 and send as string or bytes       |
| Docker: hostname error       | `[Errno -2] Name or service not known`      | Use container IP, not name, in Docker setups       |

## Testing
### Manual Test
Start a JSON server in Python:
```python
from kn_sock.json_socket import start_json_server

def handle_json(data, addr, conn):
    print("Received:", data)
    conn.sendall({"ok": True})

start_json_server(7000, handle_json)
```

Send a JSON message (in another terminal or script):
```python
from kn_sock.json_socket import send_json
print(send_json("127.0.0.1", 7000, {"test": 1}))
```

Or use CLI to send a raw JSON string:
```sh
docker-compose run --rm knsock send-tcp <server-ip> 7000 '{"test": 1}'
```