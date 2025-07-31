# Testing

This page provides instructions for testing the UDP utilities provided in `kn_sock.udp`, including synchronous, asynchronous, and multicast server-client communication.

## Test 1: Synchronous UDP Echo Server

### Step 1: Start the Server

```python
from kn_sock import start_udp_server

def echo_handler(data, addr, sock):
    print(f"Received from {addr}: {data.decode()}")
    sock.sendto(data, addr)

start_udp_server(9001, echo_handler)
```

### Step 2: Send a Message

In a second terminal or script:

```python
from kn_sock import send_udp_message

send_udp_message("127.0.0.1", 9001, "Hello UDP")
```

#### Expected Output (Server Side):

```
Received from ('127.0.0.1', <port>): Hello UDP
```

## Test 2: Asynchronous UDP Server

### Step 1: Start the Async Server

```python
import asyncio
from kn_sock import start_udp_server_async

async def echo_handler(data, addr, transport):
    print(f"Received from {addr}: {data.decode()}")
    transport.sendto(data, addr)

asyncio.run(start_udp_server_async(9002, echo_handler))
```

### Step 2: Send a Message

```python
import asyncio
from kn_sock import send_udp_message_async

async def main():
    await send_udp_message_async("127.0.0.1", 9002, "Async Hello")

asyncio.run(main())
```

#### Expected Output (Server Side):

```
Received from ('127.0.0.1', <port>): Async Hello
```

## Test 3: Multicast

### Step 1: Start the Multicast Listener

```python
from kn_sock import start_udp_multicast_server

def handler(data, addr, sock):
    print(f"[MULTICAST] {addr} says: {data.decode()}")

start_udp_multicast_server("224.0.0.1", 9003, handler)
```

### Step 2: Send a Multicast Message

```python
from kn_sock import send_udp_multicast

send_udp_multicast("224.0.0.1", 9003, "Multicast Hello")
```

#### Expected Output:

```
[MULTICAST] ('<sender_ip>', <port>) says: Multicast Hello
```

#### Note: Multicast may require local network support and may not work across Wi-Fi routers or cloud-hosted containers by default.

## Common Issues

| Error or Symptom                   | Cause                                      | Solution                                      |
|------------------------------------|--------------------------------------------|-----------------------------------------------|
| No output or response              | Handler not sending response, wrong port   | Confirm ports match and response logic is correct |
| OSError: [Errno 98] Address in use | Port already occupied                      | Use a different port or stop the existing server |
| No multicast message received      | Network or OS doesn't support multicast    | Try binding to 0.0.0.0, check firewall/network |
| OSError: [Errno 101] Network unreachable | Multicast group/route not reachable     | Make sure you're on a LAN with multicast enabled |

Having trouble with the CLI? See [Using the CLI](cli.md).

## Related Topics

- [Using the Python API](python-api.md)
- [API Reference](reference.md)