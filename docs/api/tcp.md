# TCP Utilities

kn-sock provides both CLI and Python APIs for working with TCP servers and clients.  
Use these commands to build, test, and automate network communication.

## Function Index

| Function/Class | Description |
|--|--|
| [start_tcp_server](#kn_sock.tcp.start_tcp_server) | Start a basic synchronous TCP server for single-connection, blocking I/O. Use for simple demos or network testing. |
| [start_threaded_tcp_server](#kn_sock.tcp.start_threaded_tcp_server) | Multithreaded TCP server that spawns a thread per client. Best for serving multiple simultaneous connections with blocking I/O. |
| [send_tcp_message](#kn_sock.tcp.send_tcp_message) | Synchronous TCP client: connects, sends a string, and logs the response (does not return it). For basic text protocols. |
| [send_tcp_bytes](#kn_sock.tcp.send_tcp_bytes) | Synchronous TCP client for sending raw bytes (binary payloads), logging any server response. Useful for custom protocols. |
| [start_async_tcp_server](#kn_sock.tcp.start_async_tcp_server) | Async TCP server using asyncio. Efficiently handles many connections in a single event loop. Recommended for async workloads. |
| [send_tcp_message_async](#kn_sock.tcp.send_tcp_message_async) | Async TCP client: sends a string and logs the server response without blocking. Ideal for non-blocking client logic. |
| [TCPConnectionPool](#kn_sock.tcp.TCPConnectionPool) | Thread-safe pool for managing/reusing TCP (and SSL) connections. Improves performance for high-throughput or threaded apps. |
| [start_ssl_tcp_server](#kn_sock.tcp.start_ssl_tcp_server) | Synchronous SSL/TLS TCP server, with support for client cert verification (mTLS). Use for encrypted, authenticated communication. |
| [send_ssl_tcp_message](#kn_sock.tcp.send_ssl_tcp_message) | Synchronous SSL/TLS client: connects, sends a string, logs the response. Secure text-based messaging. |
| [start_async_ssl_tcp_server](#kn_sock.tcp.start_async_ssl_tcp_server) | Async SSL/TLS TCP server using asyncio. Handles encrypted connections concurrently in a secure event loop. |
| [send_ssl_tcp_message_async](#kn_sock.tcp.send_ssl_tcp_message_async) | Async SSL/TLS client: connects, sends a string, and logs the response asynchronously. Best for secure non-blocking clients. |

## CLI Commands

### 1. Run a TCP Echo Server

Spin up a basic echo server that listens for text messages and replies with “Echo: ...”

| Command                                       | Description                   |
|-----------------------------------------------|-------------------------------|
| `run-tcp-server <port>`                       | Start a TCP echo server       |

**Example:**
```sh
docker-compose run --rm knsock run-tcp-server 8080
# Or (with pip): knsock run-tcp-server 8080
```
**Output:**
```
[TCP] Server listening on 0.0.0.0:8080
```

### 2. Send a TCP Message

Connect to a TCP server and send a text message.

| Command                                       | Description                   |
|-----------------------------------------------|-------------------------------|
| `send-tcp <host> <port> <message>`            | Send a message via TCP        |

**Example:**
```sh
docker-compose run --rm knsock send-tcp 172.18.0.2 8080 "Hello TCP"
```
**Output:**
```
[TCP] Server response: Echo: Hello TCP
```

!!! tip "How to Get the Container Name or ID"
    Run `docker ps` to list running containers. The last column (`NAMES`) is the container name.

    Example output:
    ```
    CONTAINER ID   IMAGE         ...   NAMES
    c8abcb1a321d   knsock_knsock ...  knsock_knsock_run-tcp-server_1
    ```

    Use this name or the CONTAINER ID in `docker inspect` to get the IP address.

!!! tip "How to Find the Server IP in Docker"
    Replace `172.18.0.2` with the IP address of your running TCP server container.

    You can find the container's IP by running:
    ```
    docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name_or_id>
    ```

    Use this IP as the `<host>` parameter for the `send-tcp` command.

#### Options Table
| Option        | Description                           |
|---------------|---------------------------------------|
| `<port>`      | Port number for server/client         |
| `<host>`      | IP or hostname of server (client only)|
| `<message>`   | Message to send (client only)         |

## Python API Usage Examples

### Start a TCP Server
```python
from kn_sock import start_tcp_server

def echo_handler(data, addr, conn):
    print(f"Received from {addr}: {data.decode()}")
    conn.sendall(b"Echo: " + data)

start_tcp_server(8080, echo_handler)
```

### Send a TCP Message
```python
from kn_sock import send_tcp_message
send_tcp_message('127.0.0.1', 8080, "Hello TCP")
```

### Sample Output
**Server terminal:**
```
[TCP] Server listening on 0.0.0.0:8080
[TCP][SERVER] Received from ('172.18.0.1', 49906): b'Hello TCP'
```

**Client terminal:**
```
[TCP] Server response: Echo: Hello TCP
```

## Known Issues & Troubleshooting
| Issue                        | Symptom/Output                              | Solution                                           |
|------------------------------|---------------------------------------------|----------------------------------------------------|
| Port already in use          | `OSError: [Errno 98] Address in use`        | Use a different port or kill the existing process  |
| Docker: “Connection refused” | `ConnectionRefusedError`                    | Ensure server is running and reachable             |
| Hostname not found           | `[Errno -2] Name or service not known`      | Use container IP, not name (get with `docker inspect ...`) |

## Testing
### Manual Test
In one terminal:
```sh
docker-compose run --rm knsock run-tcp-server 8080
```

In another terminal:
```sh
# Replace <server-ip> with your actual server IP
docker-compose run --rm knsock send-tcp <server-ip> 8080 "Hello TCP"
# Example:
docker-compose run --rm knsock send-tcp 172.18.0.2 8080 "Hello TCP"
```

If you see the following in your client terminal, the test passes:

`[TCP] Server response: Echo: Hello TCP`

## Python API Reference

## API Quickstart

    ... Short how-to code blocks for common usage ...

## TCP Server APIs

### Synchronous
::: kn_sock.tcp.start_tcp_server
::: kn_sock.tcp.start_threaded_tcp_server

### Asynchronous
::: kn_sock.tcp.start_async_tcp_server

## TCP Client APIs

### Synchronous
::: kn_sock.tcp.send_tcp_message
::: kn_sock.tcp.send_tcp_bytes

### Asynchronous
::: kn_sock.tcp.send_tcp_message_async

## Connection Pools

::: kn_sock.tcp.TCPConnectionPool

## SSL/TLS Server

### Synchronous
::: kn_sock.tcp.start_ssl_tcp_server

### Asynchronous
::: kn_sock.tcp.start_async_ssl_tcp_server

## SSL/TLS Client

### Synchronous
::: kn_sock.tcp.send_ssl_tcp_message

### Asynchronous
::: kn_sock.tcp.send_ssl_tcp_message_async
