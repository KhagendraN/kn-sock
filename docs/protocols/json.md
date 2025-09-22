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

## JSON Response Helpers

kn-sock provides helper functions for sending JSON responses:

### Synchronous Response

```python
from kn_sock import send_json_response

def handle_message(data, addr, client_socket):
    # Process the message...
    
    # Send a JSON response
    response_data = {
        "status": "success",
        "result": "processed",
        "timestamp": time.time()
    }
    send_json_response(client_socket, response_data)
```

### Asynchronous Response

```python
from kn_sock import send_json_response_async

async def handle_message(data, addr, writer):
    # Process the message...
    
    # Send a JSON response
    response_data = {
        "status": "success",
        "result": "processed",
        "timestamp": time.time()
    }
    await send_json_response_async(writer, response_data)
```

## Error Handling

### Invalid JSON Handling

```python
from kn_sock.errors import InvalidJSONError

def handle_json_message(data, addr, client_socket):
    try:
        # Process JSON data
        message_type = data.get('type')
        # ... rest of processing
    except InvalidJSONError as e:
        error_response = {
            "error": "invalid_json",
            "message": str(e)
        }
        send_json_response(client_socket, error_response)
```

### Timeout Handling

```python
from kn_sock.errors import ConnectionTimeoutError

try:
    response = send_json("localhost", 8080, data, timeout=5)
except ConnectionTimeoutError:
    print("Request timed out")
except Exception as e:
    print(f"Error: {e}")
```

## Use Cases

### API-like Communication

```python
# Server
def handle_api_request(data, addr, client_socket):
    endpoint = data.get('endpoint')
    params = data.get('params', {})
    
    if endpoint == 'get_user':
        user_id = params.get('user_id')
        user = get_user_by_id(user_id)  # Your function
        response = {"status": "success", "data": user}
    elif endpoint == 'create_user':
        user_data = params.get('user_data')
        new_user = create_user(user_data)  # Your function
        response = {"status": "success", "data": new_user}
    else:
        response = {"status": "error", "message": "Unknown endpoint"}
    
    send_json_response(client_socket, response)

# Client
def get_user(user_id):
    request = {
        "endpoint": "get_user",
        "params": {"user_id": user_id}
    }
    send_json("localhost", 8080, request)
```

### Configuration Exchange

```python
# Server
def handle_config_request(data, addr, client_socket):
    config_type = data.get('config_type')
    
    configs = {
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'myapp'
        },
        'redis': {
            'host': 'localhost',
            'port': 6379
        }
    }
    
    config = configs.get(config_type, {})
    response = {"config": config}
    send_json_response(client_socket, response)

# Client
def get_config(config_type):
    request = {"config_type": config_type}
    send_json("localhost", 8080, request)
```

### Event Broadcasting

```python
# Server
def handle_event(data, addr, client_socket):
    event_type = data.get('event_type')
    event_data = data.get('event_data')
    
    # Broadcast to all connected clients
    broadcast_event = {
        "type": "broadcast",
        "event_type": event_type,
        "event_data": event_data,
        "timestamp": time.time()
    }
    
    # Send to all clients (implementation depends on your client tracking)
    for client in connected_clients:
        send_json_response(client, broadcast_event)

# Client
def send_event(event_type, event_data):
    event = {
        "event_type": event_type,
        "event_data": event_data
    }
    send_json("localhost", 8080, event)
```

## Advanced Patterns

### Request-Response with Correlation

```python
import uuid

# Client
def send_request_with_correlation(endpoint, params):
    correlation_id = str(uuid.uuid4())
    request = {
        "correlation_id": correlation_id,
        "endpoint": endpoint,
        "params": params,
        "timestamp": time.time()
    }
    send_json("localhost", 8080, request)
    return correlation_id

# Server
def handle_correlated_request(data, addr, client_socket):
    correlation_id = data.get('correlation_id')
    endpoint = data.get('endpoint')
    params = data.get('params')
    
    # Process request...
    result = process_request(endpoint, params)
    
    response = {
        "correlation_id": correlation_id,
        "status": "success",
        "result": result,
        "timestamp": time.time()
    }
    send_json_response(client_socket, response)
```

### Batch Operations

```python
# Client
def send_batch_operations(operations):
    batch = {
        "type": "batch",
        "operations": operations,
        "batch_id": str(uuid.uuid4())
    }
    send_json("localhost", 8080, batch)

# Server
def handle_batch_operations(data, addr, client_socket):
    operations = data.get('operations', [])
    batch_id = data.get('batch_id')
    
    results = []
    for op in operations:
        result = process_operation(op)
        results.append(result)
    
    response = {
        "type": "batch_response",
        "batch_id": batch_id,
        "results": results
    }
    send_json_response(client_socket, response)
```

## Validation and Decorators

kn-sock provides decorators for JSON validation:

```python
from kn_sock.decorators import ensure_json_input

@ensure_json_input
def handle_json_message(data, addr, client_socket):
    # data is guaranteed to be a valid JSON object (dict)
    message_type = data.get('type')
    # ... rest of processing
```

## Performance Considerations

### Large JSON Objects

For large JSON objects, consider compression:

```python
from kn_sock.compression import compress_data, decompress_data

# Client
def send_large_json(data):
    json_str = json.dumps(data)
    compressed = compress_data(json_str.encode('utf-8'))
    send_tcp_bytes("localhost", 8080, compressed)

# Server
def handle_compressed_json(data, addr, client_socket):
    decompressed = decompress_data(data)
    json_data = json.loads(decompressed.decode('utf-8'))
    # Process json_data...
```

### Streaming JSON

For very large datasets, consider streaming:

```python
def send_json_stream(host, port, data_generator):
    for chunk in data_generator:
        json_chunk = json.dumps(chunk)
        send_tcp_message(host, port, json_chunk)
```

## CLI Usage

```bash
# Send JSON data via CLI
kn-sock send-json localhost 8080 '{"message": "Hello", "type": "greeting"}'
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