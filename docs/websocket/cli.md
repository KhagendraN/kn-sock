# Websocket: Using the CLI

`kn‑sock` exposes basic WebSocket helpers under the `knsock websocket` namespace.
They are thin wrappers around the Python API, ideal for smoke tests or shell
scripts.

| Command                                  | Description                   |
|------------------------------------------|-------------------------------|
| `knsock websocket run-server <port>`     | Start an echo server on `<port>` |
| `knsock websocket send <host> <port> <msg>` | Connect, send a text frame, print the reply |

## Examples

### Start an echo server on 8765

```bash
docker-compose run --rm knsock websocket run-server 8765
```

Output:

```csharp
[WebSocket][SERVER] Listening on 0.0.0.0:8765
```

### Send a single frame

```bash
docker-compose run --rm knsock \
  websocket send localhost 8765 "hello from cli"
```

Output:

```css
[WebSocket][CLIENT] → hello from cli
[WebSocket][CLIENT] ← Echo: hello from cli
```

## Options

| Flag | Description |
|------|-------------|
| --headers | Additional HTTP headers (key:value) |
| --resource | WebSocket path (default /) |
| --timeout | Seconds to wait before exit (default 5) |

### Positional Arguments

| Argument     | Description                            |
|--------------|----------------------------------------|
| `<host>`     | IP address or hostname of the server   |
| `<port>`     | Port number to connect to or bind on   |
| `<message>`  | Message to send (for `send` command)   |

!!! note
    These commands are wrappers around `start_websocket_server()` and `connect_websocket()`. For advanced workflows, see [Using the Python API](python-api.md).

## Related Topics

- [Using the Python API](python-api.md)
- [API Reference](reference.md)
- [Testing & Troubleshooting](testing.md)