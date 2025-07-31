# WebSocket Python API

The kn‑sock WebSocket API supports both synchronous and asynchronous usage. Use it for custom WebSocket servers, real‑time clients, or automation tools.

## Start a WebSocket Server

```python
from kn_sock.websocket import start_websocket_server, WebSocketConnection
import threading

def echo_handler(ws: WebSocketConnection):
    while ws.open:
        msg = ws.recv()
        if msg:
            ws.send(f"Echo: {msg}")

shutdown = threading.Event()

start_websocket_server(
    host="0.0.0.0",
    port=8765,
    handler=echo_handler,
    shutdown_event=shutdown
)
```

Use shutdown.set() in another thread to stop the server gracefully.

## Connect as a Client (Sync)

```python
from kn_sock.websocket import connect_websocket

ws = connect_websocket("localhost", 8765)
ws.send("Hello!")
print(ws.recv())  # Echo: Hello!
ws.close()
```

## Connect as a Client (Async)

```python
import asyncio
from kn_sock.websocket import async_connect_websocket

async def run():
    ws = await async_connect_websocket("localhost", 8765)
    await ws.send("Ping")
    reply = await ws.recv()
    print(reply)
    await ws.close()

asyncio.run(run())
```

## Notes

- Both client types return a WebSocketConnection object with .send(), .recv(), and .close() methods.
- Messages are UTF‑8 strings.
- Servers support threading by default.

## Related Topics

- [Using the CLI](cli.md)
- [API Reference](reference.md)
- [Testing & Troubleshooting](testing.md)