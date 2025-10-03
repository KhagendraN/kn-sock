# Error Handling

kn-sock provides custom exception classes for better error handling in socket applications.

## Exception Hierarchy

All kn-sock exceptions inherit from `EasySocketError`:

```python
from kn_sock.errors import EasySocketError, ConnectionTimeoutError, PortInUseError

try:
    # Socket operations
    pass
except EasySocketError as e:
    # Catches all kn-sock errors
    print(f"Socket error: {e}")
```

## Available Exceptions

### `EasySocketError`
Base exception for all kn-sock errors.

### `ConnectionTimeoutError(message="Connection timed out.")`
Raised when connection or I/O operations time out.

### `PortInUseError(port, message=None)`
Raised when a specified port is already in use.

**Parameters:**
- `port` (int): The port number that's in use
- `message` (str, optional): Custom error message

### `InvalidJSONError(message="Received invalid JSON data.")`
Raised when JSON message cannot be decoded.

### `UnsupportedProtocolError(protocol, message=None)`
Raised when a requested protocol is not supported.

**Parameters:**
- `protocol` (str): The unsupported protocol name
- `message` (str, optional): Custom error message

### `FileTransferError(message="File transfer failed.")`
Raised when file transfer operations fail.

## Usage Examples

```python
from kn_sock import start_tcp_server
from kn_sock.errors import PortInUseError, ConnectionTimeoutError

# Handle port conflicts
try:
    start_tcp_server(8080, handler)
except PortInUseError as e:
    print(f"Port conflict: {e}")

# Handle timeouts
try:
    send_tcp_message("localhost", 8080, "Hello")
except ConnectionTimeoutError:
    print("Server is not responding")
```
