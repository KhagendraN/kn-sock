# WebSocket Utilities

`kn‑sock` adds a full‑duplex WebSocket layer on top of its HTTP helpers.  
Use it to build lightweight chat servers, real‑time dashboards, or any
application that benefits from persistent, bidirectional messaging.

Choose the interface that fits your workflow:

- **CLI** Run quick echo servers or send one‑off frames from the terminal.  
- **Python API** Embed servers or clients directly in your code (sync *or* async).

## Function Index

| Function / Class | Description |
|------------------|-------------|
| [start_websocket_server](reference.md#kn_sock.websocket.start_websocket_server) | Thread‑per‑client synchronous WebSocket server |
| [connect_websocket](reference.md#kn_sock.websocket.connect_websocket) | Blocking client, returns `WebSocketConnection` |
| [WebSocketConnection](reference.md#kn_sock.websocket.WebSocketConnection) | Sync connection object (`send / recv / close`) |
| [async_connect_websocket](reference.md#kn_sock.websocket.async_connect_websocket) | Asyncio client, returns `AsyncWebSocketConnection` |
| [AsyncWebSocketConnection](reference.md#kn_sock.websocket.AsyncWebSocketConnection) | Async connection object (`await send / recv / close`) |

## When to Use WebSockets

- Real‑time dashboards, chat, or collaborative apps  
- Low‑latency, event‑driven messaging without HTTP request overhead  
- Client‑ and server‑initiated pushes over the same TCP socket  

For simple request/response APIs, refer to [HTTP Utilities](../http/index.md).

## Quick Start

### 1 · Run an echo server

```python
from kn_sock.websocket import start_websocket_server, WebSocketConnection

def echo(ws: WebSocketConnection):
    while ws.open:
        msg = ws.recv()
        if msg:
            ws.send(f"Echo: {msg}")

start_websocket_server("0.0.0.0", 8765, echo)
```

### 2 · Connect (sync)

```python
from kn_sock.websocket import connect_websocket
ws = connect_websocket("localhost", 8765)
ws.send("hello")
print(ws.recv())     # → Echo: hello
ws.close()
```

### 3 · Connect (async)

```python
import asyncio
from kn_sock.websocket import async_connect_websocket

async def main():
    ws = await async_connect_websocket("localhost", 8765)
    await ws.send("ping")
    print(await ws.recv())  # → Echo: ping
    await ws.close()

asyncio.run(main())
```

## Common Options

| Option | Description |
|--------|-------------|
| host | IP or hostname of the server |
| port | Port number (default 8765 in examples) |
| resource | URL path (default /) |
| headers | Extra HTTP headers for the handshake |

## Known Issues & Troubleshooting

| Symptom / Error | Likely Cause / Fix |
|-----------------|---------------------|
| ConnectionError – handshake failed | Wrong port, proxy in the way, or bad Host header |
| EOFError inside recv() | Client closed socket mid‑frame |
| UnicodeDecodeError on recv() | Non‑UTF‑8 payload received |

## Related Topics

- [Using the CLI](cli.md)
- [Using the Python API](python-api.md)
- [API Reference](reference.md)
- [Testing & Troubleshooting](testing.md)