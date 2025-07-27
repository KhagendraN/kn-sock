# Testing

This page provides manual test instructions to verify your TCP setup using either the CLI or Python API. These tests confirm that both the server and client components are functioning correctly and communicating over the network.

## Test 1: Using Docker CLI

### Step 1: Start a TCP Echo Server

In one terminal window:

```bash
docker-compose run --rm knsock run-tcp-server 8080
```

#### Expected output:

```
[TCP] Server listening on 0.0.0.0:8080
```

### Step 2: Send a Message from a Client

In another terminal window:

```bash
# Replace <server-ip> with the container's IP address
docker-compose run --rm knsock send-tcp <server-ip> 8080 "Hello TCP"
```

#### Example:

```bash
docker-compose run --rm knsock send-tcp 172.18.0.2 8080 "Hello TCP"
```

#### Expected output:

```
[TCP] Server response: Echo: Hello TCP
```

### How to Find the Container IP

If you do not know the `<server-ip>`, run:

```bash
docker ps
```

Then inspect the server container:

```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name_or_id>
```

Use the resulting IP address as the host for your client command.

---

## Test 2: Using Python

### Start the server in one terminal:

```python
# server.py
from kn_sock import start_tcp_server

def echo_handler(data, addr, conn):
    print(f"Received from {addr}: {data.decode()}")
    conn.sendall(b"Echo: " + data)

start_tcp_server(8080, echo_handler)
```

### Then run the client from another terminal:

```python
# client.py
from kn_sock import send_tcp_message

send_tcp_message("127.0.0.1", 8080, "Hello TCP")
```

#### Expected output in the server terminal:

```
[TCP] Server listening on 0.0.0.0:8080
[TCP][SERVER] Received from ('127.0.0.1', 50000): b'Hello TCP'
```

#### Expected output in the client terminal:

```
[TCP] Server response: Echo: Hello TCP
```

---

## Common Errors

| Error               | Message or Symptom                     | Fix                                      |
|---------------------|---------------------------------------|------------------------------------------|
| Port already in use | `OSError: [Errno 98] Address in use`  | Use a different port or stop the conflicting process |
| Server not responding | `ConnectionRefusedError`             | Verify that the server is running and reachable |
| DNS resolution failed (Docker) | `Name or service not known`          | Use the container IP address instead of the container name |
| No response or empty output | No logs or messages received         | Confirm that port numbers match and the server is properly configured |

---

## Optional: Add Test Script

You can create a basic test script to automate verification:

```bash
python test_tcp_connection.py
```

#### Example test_tcp_connection.py:

```python
from kn_sock import send_tcp_message

try:
    send_tcp_message("127.0.0.1", 8080, "Ping")
    print("TCP test passed")
except Exception as e:
    print(f"TCP test failed: {e}")
```

---

## Next Steps

- [Using the CLI](#)
- [Using the Python API](#)
- [API Reference](#)