# JSON Communication

kn-sock provides built-in support for JSON communication, making it easy to send and receive structured data over sockets.

## Overview

JSON communication in kn-sock:
- Automatically serializes Python objects to JSON
- Handles encoding/decoding transparently
- Supports both synchronous and asynchronous operations
- Provides error handling for invalid JSON
- Works over both TCP and UDP

## Basic JSON Communication

### JSON Server

```python
from kn_sock import start_json_server

def handle_json_message(data, addr, client_socket):
    """
    Handle incoming JSON messages.

    Args:
        data (dict): The JSON data received from the client.
        addr (tuple): The address of the client.
        client_socket (socket.socket): The client socket.
    """
    print(f"Received from {addr}: {data}")
    
    # Process the JSON data
    message_type = data.get('type')
    payload = data.get('payload')
    
    # Send a JSON response
    response = {
        "status": "received",
        "message_type": message_type,
        "timestamp": time.time()
    }
    client_socket.sendall(json.dumps(response).encode('utf-8'))

start_json_server(8080, handle_json_message)
```

### JSON Client

```python
from kn_sock import send_json

# Send a simple JSON object
message = {"message": "Hello, World!"}
send_json("localhost", 8080, message)

# Send a complex JSON object
data = {
    "type": "user_data",
    "payload": {
        "user_id": 123,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "timestamp": time.time()
}
send_json("localhost", 8080, data)
```

## Asynchronous JSON Communication

### Async JSON Server

```python
import asyncio
from kn_sock import start_json_server_async

async def handle_json_message(data, addr, writer):
    """
    Handle incoming JSON messages asynchronously.

    Args:
        data (dict): The JSON data received from the client.
        addr (tuple): The address of the client.
        writer (asyncio.StreamWriter): The writer object for the client.
    """
    print(f"Received from {addr}: {data}")
    
    response = {"status": "received", "data": data}
    writer.write(json.dumps(response).encode('utf-8'))
    await writer.drain()

asyncio.run(start_json_server_async(8080, handle_json_message))
```

### Async JSON Client

```python
import asyncio
from kn_sock import send_json_async

async def main():
    data = {"message": "Hello, async JSON!"}
    await send_json_async("localhost", 8080, data)

asyncio.run(main())
```
## Best Practices

1. **Use consistent message structure**: Define a standard format for your JSON messages
2. **Include timestamps**: Add timestamps for debugging and logging
3. **Handle errors gracefully**: Always provide meaningful error responses
4. **Validate input**: Use decorators or manual validation for critical data
5. **Use correlation IDs**: For request-response patterns, include correlation IDs
6. **Consider compression**: For large JSON objects, use compression
7. **Document your API**: Clearly document the expected JSON structure

## Related Topics

- **[TCP Protocol](tcp.md)** - For reliable JSON communication
- **[UDP Protocol](udp.md)** - For fast JSON messaging
- **[File Transfer](file-transfer.md)** - For large data transfer
- **[API Reference](../api-reference.md)** - Complete function documentation 