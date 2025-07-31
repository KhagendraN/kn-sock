# TCP: Using the CLI

The `knsock` command-line interface allows you to start TCP servers and send messages over TCP directly from the shell. It's ideal for testing or scripting quick network interactions without writing Python code.

## Run a TCP Echo Server

Start a server that echoes back any received messages.

### Command

```bash
knsock run-tcp-server <port>
```

Or using Docker:

```bash
docker-compose run --rm knsock run-tcp-server 8080
```

#### Example Output

```
[TCP] Server listening on 0.0.0.0:8080
```

## Send a TCP Message

Connect to a TCP server and send a UTF-8 string message.

### Command

```bash
knsock send-tcp <host> <port> <message>
```

Or using Docker:

```bash
docker-compose run --rm knsock send-tcp <host> <port> <message>
```

#### Example

```bash
docker-compose run --rm knsock send-tcp 172.18.0.2 8080 "Hello TCP"
```

#### Example Output

```
[TCP] Server response: Echo: Hello TCP
```

## CLI Options

| Argument  | Description                              |
|-----------|------------------------------------------|
| `<port>`  | Port to bind for the server or connect to |
| `<host>`  | IP or hostname of the TCP server (client only) |
| `<message>` | Text to send to the server (client only) |

## Getting the Server IP (Docker)

If you're running the TCP server in a Docker container, you’ll need its internal IP to connect from the client.

### Step 1: List Running Containers

```bash
docker ps
```

Look for the NAMES column, e.g.:

```
CONTAINER ID   IMAGE         ...   NAMES
c8abcb1a321d   knsock_knsock ...  knsock_knsock_run-tcp-server_1
```

### Step 2: Get the Container's IP Address

```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name_or_id>
```

Use this IP as the `<host>` value when calling `send-tcp`.

## Troubleshooting

| Issue              | Error or Output                     | Suggested Fix                          |
|--------------------|-------------------------------------|----------------------------------------|
| Port already in use | `OSError: [Errno 98] Address in use` | Choose a different port or stop the running server |
| Connection refused  | `ConnectionRefusedError`            | Ensure the server is running and accepting connections |
| Hostname not found  | `[Errno -2] Name or service not known` | Use the container IP instead of the name |

## Related Topics

- [Using the Python API](python-api.md)
- [Full TCP Function Reference](reference.md)
- [Testing Instructions](testing.md)