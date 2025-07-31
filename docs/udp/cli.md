# UDP: Using the CLI

The `knsock` command‑line interface now includes a set of **synchronous** UDP commands for rapid testing and lightweight messaging.

All commands run inside the same Typer‑based CLI you use for TCP.

!!! note
    These commands are synchronous.  
    Asynchronous UDP helpers (e.g., `start_udp_server_async`) are available only in the Python API.

## Run a UDP Echo Server

Starts a UDP echo server that listens for datagrams and sends each message back to the sender.

| Command                                 | Description                   |
|-----------------------------------------|-------------------------------|
| `knsock udp run-udp-server <port>`      | Start a UDP echo server       |

### Example

```bash
# Using pip‑installed knsock
knsock udp run-udp-server 8081

# Or inside Docker
docker-compose run --rm knsock knsock udp run-udp-server 8081
```

Expected output:

```csharp
[UDP][SYNC] Server listening on 0.0.0.0:8081
```

## Send a UDP Message

Sends a UTF‑8 datagram to a running UDP server.

| Command | Description |
|---------|-------------|
| `knsock udp send-udp <host> <port> <msg>` | Send a UDP datagram |

### Example

```bash
knsock udp send-udp 127.0.0.1 8081 "Hello UDP"
```

Expected output:

```css
[UDP][SYNC] Sent to 127.0.0.1:8081
```

## Run a UDP Multicast Server

Listens for multicast datagrams on a group and port, then echoes each message back.

| Command | Description |
|---------|-------------|
| `knsock udp run-udp-multicast-server <group> <port>` | Start a multicast listener |

### Example

```bash
knsock udp run-udp-multicast-server 224.0.0.1 9000
```

Expected output:

```csharp
[UDP][MULTICAST] Listening on group 224.0.0.1:9000
```

## Send a Multicast Message

Sends a multicast datagram to a group and port.

| Command | Description |
|---------|-------------|
| `knsock udp send-udp-multicast <group> <port> <msg> [--ttl <n>]` | Send a multicast datagram |

### Example

```bash
knsock udp send-udp-multicast 224.0.0.1 9000 "Multicast Hello"
```

Expected output:

```css
[UDP][SYNC] Sent to 224.0.0.1:9000
```

## Options

| Option / Argument | Description |
|-------------------|-------------|
| `<port>` | Port for the server or destination port for the client |
| `<host>` | Destination IP or hostname for send-udp |
| `<message>` | UTF‑8 message to send |
| `<group>` | Multicast group IP (e.g., 224.0.0.1) |
| `--host` | Host/IP to bind the server (default 0.0.0.0) |
| `--listen-ip` | Local interface for multicast server (default 0.0.0.0) |
| `--ttl` | Multicast TTL (default 1) |

## CLI Troubleshooting

| Issue / Error                      | Likely Cause                    | Suggested Fix                                  |
|------------------------------------|---------------------------------|------------------------------------------------|
| Command not found                  | CLI not installed or PATH issue | Confirm knsock is installed and PATH is set    |
| Argument parsing failed            | Wrong order or missing args     | Check command syntax and required arguments    |
| OSError: [Errno 98] Address in use | Port already in use             | Stop other server or choose another port       |
| Permission denied                  | Insufficient privileges         | Use sudo (Linux) or run as admin (Windows)     |

For UDP protocol/network issues, see [Testing & Troubleshooting](testing.md).

## Quick CLI Test

Open two terminals:

Start the server  
```sh
docker-compose run --rm knsock udp run-udp-server 8081
```

Send a message

```sh
docker-compose run --rm knsock udp send-udp 127.0.0.1 8081 "Hello UDP"
```

Expected output

**Server**

```less
[UDP][SYNC] Listening on 0.0.0.0:8081
[UDP][SYNC] Received from ('<client-ip>'): Hello UDP
```

**Client**

```css
[UDP][SYNC] Sent to 127.0.0.1:8081
```

If it fails

- Verify you used the correct IP and port
- Check that both processes share the same Docker network (or use 127.0.0.1 outside Docker)
- Confirm no firewall is blocking UDP on 8081

## Related Topics

- [Using the Python API](python-api.md)
- [API Reference](reference.md)
- [Testing & Troubleshooting](testing.md)