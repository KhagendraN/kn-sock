# Decorators

kn-sock provides a collection of useful decorators to enhance your socket programming workflow. These decorators help with error handling, performance monitoring, retry logic, and data validation.

## Overview

The decorators module includes:
- **Exception logging** - Automatic logging of exceptions with optional re-raising
- **Retry logic** - Automatic retry with configurable delays and exception types
- **Performance monitoring** - Execution time measurement and logging
- **JSON validation** - Ensure handler functions receive valid JSON data

## Exception Logging

### `@log_exceptions`

Automatically logs exceptions that occur in decorated functions, with optional re-raising.

```python
from kn_sock.decorators import log_exceptions

@log_exceptions(raise_error=True)
def handle_client_message(data, addr, socket):
    """Handler that logs exceptions automatically"""
    # Process message - any exceptions will be logged
    result = process_message(data)
    socket.sendall(result.encode())

# Usage with TCP server
from kn_sock import start_tcp_server
start_tcp_server(8080, handle_client_message)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `raise_error` | bool | `True` | Whether to re-raise the exception after logging |

#### Behavior

- **With `raise_error=True`**: Logs the exception and re-raises it
- **With `raise_error=False`**: Logs the exception and continues execution

```python
@log_exceptions(raise_error=False)
def tolerant_handler(data, addr, socket):
    """Handler that continues despite errors"""
    # Errors are logged but don't crash the server
    pass

@log_exceptions(raise_error=True)  # Default behavior
def strict_handler(data, addr, socket):
    """Handler that stops on errors"""
    # Errors are logged and re-raised
    pass
```

## Retry Logic

### `@retry`

Automatically retries functions that fail, with configurable retry count, delay, and exception types.

```python
from kn_sock.decorators import retry
import requests

@retry(retries=3, delay=1.0, exceptions=(ConnectionError, TimeoutError))
def send_to_external_api(data):
    """Function that retries on network errors"""
    response = requests.post('https://api.example.com/data', json=data)
    return response.json()

# Usage in handler
def handle_message(data, addr, socket):
    try:
        result = send_to_external_api(data)
        socket.sendall(json.dumps(result).encode())
    except Exception as e:
        socket.sendall(f"Failed after retries: {e}".encode())
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `retries` | int | `3` | Maximum number of retry attempts |
| `delay` | float | `1.0` | Delay in seconds between retries |
| `exceptions` | tuple | `(Exception,)` | Tuple of exception types to catch and retry |

#### Advanced Usage

```python
# Retry only specific exceptions
@retry(retries=5, delay=2.0, exceptions=(ConnectionError, socket.timeout))
def network_operation():
    # Only retries on connection errors and timeouts
    pass

# Quick retries with no delay
@retry(retries=3, delay=0)
def fast_retry_operation():
    pass

# Retry all exceptions (default)
@retry(retries=2)
def retry_everything():
    pass
```

## Performance Monitoring

### `@measure_time`

Measures and logs the execution time of decorated functions.

```python
from kn_sock.decorators import measure_time

@measure_time
def process_large_dataset(data):
    """Function with performance monitoring"""
    # Complex processing...
    result = expensive_computation(data)
    return result

# Usage in server handler
@measure_time
def handle_file_upload(data, addr, socket):
    """Handler with timing"""
    processed_data = process_large_dataset(data)
    socket.sendall(processed_data)
```

#### Output

The decorator logs execution time using the standard Python logging system:

```
INFO:kn_sock.decorators:[TIMER] process_large_dataset executed in 2.3456 seconds
INFO:kn_sock.decorators:[TIMER] handle_file_upload executed in 0.1234 seconds
```

#### Configuration

Configure logging level to control timer output:

```python
import logging
logging.getLogger('kn_sock.decorators').setLevel(logging.INFO)
```

## JSON Validation

### `@ensure_json_input`

Validates that the first argument to a function is valid JSON data (dict or JSON string).

```python
from kn_sock.decorators import ensure_json_input

@ensure_json_input
def handle_json_message(data, addr, socket):
    """Handler that expects JSON input"""
    # data is guaranteed to be a dict at this point
    message_type = data.get('type')
    payload = data.get('payload')
    
    response = {"status": "received", "type": message_type}
    socket.sendall(json.dumps(response).encode())

# Usage with JSON server
from kn_sock import start_json_server
start_json_server(8080, handle_json_message)
```

#### Behavior

- **Dict input**: Passes through unchanged
- **Valid JSON string**: Automatically parsed to dict
- **Invalid JSON string**: Raises `InvalidJSONError`
- **Other types**: Raises `InvalidJSONError`

#### Error Handling

```python
from kn_sock.errors import InvalidJSONError

@ensure_json_input
def safe_json_handler(data, addr, socket):
    try:
        # Process validated JSON data
        result = process_json_data(data)
        socket.sendall(json.dumps(result).encode())
    except InvalidJSONError as e:
        error_response = {"error": "invalid_json", "message": str(e)}
        socket.sendall(json.dumps(error_response).encode())
```

## Combining Decorators

Decorators can be stacked for comprehensive error handling and monitoring:

```python
from kn_sock.decorators import log_exceptions, retry, measure_time, ensure_json_input

@log_exceptions(raise_error=False)  # Log but don't crash
@retry(retries=2, delay=0.5)        # Retry on failures
@measure_time                       # Monitor performance
@ensure_json_input                  # Validate JSON input
def robust_handler(data, addr, socket):
    """Fully decorated handler with all features"""
    
    # Process the validated JSON data
    message_type = data.get('type')
    
    if message_type == 'ping':
        response = {"type": "pong", "timestamp": time.time()}
    else:
        response = {"error": "unknown_message_type"}
    
    socket.sendall(json.dumps(response).encode())

# Usage
from kn_sock import start_json_server
start_json_server(8080, robust_handler)
```

## Real-World Examples

### Resilient API Handler

```python
import time
import json
from kn_sock.decorators import log_exceptions, retry, measure_time, ensure_json_input

@log_exceptions(raise_error=False)
@retry(retries=3, delay=1.0, exceptions=(ConnectionError, TimeoutError))
@measure_time
@ensure_json_input
def api_handler(data, addr, socket):
    """Production-ready API handler"""
    
    endpoint = data.get('endpoint')
    params = data.get('params', {})
    
    if endpoint == 'get_user':
        user = fetch_user_from_db(params.get('user_id'))
        response = {"status": "success", "data": user}
        
    elif endpoint == 'process_data':
        result = process_data_with_external_service(params)
        response = {"status": "success", "result": result}
        
    else:
        response = {"status": "error", "message": "Unknown endpoint"}
    
    socket.sendall(json.dumps(response).encode())
```

### File Processing Handler

```python
@log_exceptions()
@measure_time
def file_processor_handler(data, addr, socket):
    """Handler for file processing operations"""
    
    try:
        # Process uploaded file data
        processed_file = process_file_data(data)
        
        # Save to storage
        file_id = save_to_storage(processed_file)
        
        response = {
            "status": "success", 
            "file_id": file_id,
            "size": len(processed_file)
        }
        
    except Exception as e:
        response = {"status": "error", "message": str(e)}
    
    socket.sendall(json.dumps(response).encode())
```

### Chat Server Handler

```python
@log_exceptions(raise_error=False)  # Keep server running
@ensure_json_input
def chat_handler(data, addr, socket):
    """Chat server message handler"""
    
    message_type = data.get('type')
    username = data.get('username')
    content = data.get('content')
    
    if message_type == 'join':
        add_user_to_chat(username, socket)
        broadcast_message(f"{username} joined the chat")
        
    elif message_type == 'message':
        broadcast_message(f"{username}: {content}")
        
    elif message_type == 'leave':
        remove_user_from_chat(username)
        broadcast_message(f"{username} left the chat")
```

## Best Practices

### 1. Decorator Order

When stacking decorators, consider the order:

```python
# Recommended order (bottom to top):
@log_exceptions()      # Outermost - catches all errors
@retry()              # Retry logic
@measure_time         # Performance monitoring
@ensure_json_input    # Input validation (innermost)
def handler(data, addr, socket):
    pass
```

### 2. Exception Handling Strategy

```python
# For critical services - fail fast
@log_exceptions(raise_error=True)
@retry(retries=1)  # Minimal retries
def critical_handler(data, addr, socket):
    pass

# For resilient services - keep running
@log_exceptions(raise_error=False)
@retry(retries=5, delay=2.0)
def resilient_handler(data, addr, socket):
    pass
```

### 3. Performance Monitoring

Use `@measure_time` selectively on operations you want to monitor:

```python
@measure_time
def expensive_operation(data):
    # Only monitor time-critical functions
    pass

def simple_operation(data):
    # Don't monitor simple operations
    pass
```

### 4. Logging Configuration

Configure logging appropriately for your environment:

```python
import logging

# Development - see all decorator logs
logging.getLogger('kn_sock.decorators').setLevel(logging.DEBUG)

# Production - only errors and warnings
logging.getLogger('kn_sock.decorators').setLevel(logging.WARNING)
```

## Error Types

The decorators module uses these error types:

- **`InvalidJSONError`**: Raised by `@ensure_json_input` for invalid JSON data
- **Standard Python exceptions**: Handled by `@retry` and `@log_exceptions`

## Related Topics

- **[Error Handling](api-reference.md#error-handling)** - Complete error handling reference
- **[TCP Protocol](protocols/tcp.md)** - Using decorators with TCP servers
- **[JSON Communication](protocols/json.md)** - JSON validation with decorators
- **[Configuration](configuration.md)** - Logging configuration options
