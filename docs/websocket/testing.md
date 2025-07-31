# Testing WebSocket Utilities

## Manual Test

```bash
# In one terminal, run:
python3 websocket_server.py

# In another terminal, test with Python:
from kn_sock.websocket import connect_websocket
ws = connect_websocket("localhost", 8765)
ws.send("ping")
print(ws.recv())
```

## Automated Test

```python
import threading
import time
from kn_sock.websocket import start_websocket_server, connect_websocket

def echo(ws):
    while ws.open:
        msg = ws.recv()
        if msg:
            ws.send(msg)

def test_websocket_echo():
    shutdown = threading.Event()
    thread = threading.Thread(
        target=start_websocket_server,
        kwargs={"host": "127.0.0.1", "port": 9000, "handler": echo, "shutdown_event": shutdown},
        daemon=True
    )
    thread.start()
    time.sleep(0.5)
    ws = connect_websocket("127.0.0.1", 9000)
    ws.send("test")
    assert ws.recv() == "test"
    ws.close()
    shutdown.set()
    thread.join(timeout=1)

test_websocket_echo()
```

## Expected Output

**Server terminal:**
```sh
[WebSocket][SERVER] Listening on 0.0.0.0:9000
[WebSocket][SERVER] Connection from ('172.18.0.1', 33512)
[WebSocket][SERVER] Received: Hello WebSocket
```

```sh
[WebSocket][SERVER] Listening on 0.0.0.0:9000
[WebSocket][SERVER] Connection from ('172.18.0.1', 33512)
[WebSocket][SERVER] Received: Hello WebSocket
```

**Client terminal:**
```sh
[WebSocket][CLIENT] Connected to ws://172.18.0.2:9000
[WebSocket][CLIENT] Sent: Hello WebSocket
[WebSocket][CLIENT] Received: Echo: Hello WebSocket
```

You can adapt IP addresses or messages as needed, but this serves as a helpful baseline for smoke tests or support.

## Related Topics

- [Using the CLI](cli.md)
- [Using the Python API](python-api.md)
- [API Reference](reference.md)