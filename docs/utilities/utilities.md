# Utilities

Network and file utilities for socket programming.

## Network Functions

### `get_free_port()`
Find an available TCP port.

**Returns:** int - Available port number

**Example:**
```python
from kn_sock.utils import get_free_port

port = get_free_port()
start_tcp_server(port, handler)
```

### `get_local_ip()`
Get the local IP address of the machine.

**Returns:** str - Local IP address

**Example:**
```python
from kn_sock.utils import get_local_ip

ip = get_local_ip()
print(f"Server running on {ip}:8080")
```

## File Functions

### `chunked_file_reader(filepath, chunk_size=4096)`
Read file data in chunks for streaming.

**Parameters:**
- `filepath` (str): Path to file
- `chunk_size` (int): Chunk size in bytes (default: 4096)

**Returns:** Generator yielding bytes

**Example:**
```python
from kn_sock.utils import chunked_file_reader

for chunk in chunked_file_reader("large_file.bin"):
    socket.send(chunk)
```

### `recv_all(socket, total_bytes)`
Receive exactly the specified number of bytes.

**Parameters:**
- `socket` (socket.socket): Socket to read from
- `total_bytes` (int): Number of bytes to receive

**Returns:** bytes - Received data

**Example:**
```python
from kn_sock.utils import recv_all

# Receive file size first (4 bytes)
size_data = recv_all(socket, 4)
file_size = int.from_bytes(size_data, 'big')

# Receive entire file
file_data = recv_all(socket, file_size)
```

## Display Functions

### `print_progress(received, total)`
Print file transfer progress.

**Parameters:**
- `received` (int): Bytes received so far
- `total` (int): Total bytes expected

**Example:**
```python
from kn_sock.utils import print_progress

total_size = 1000000
received = 0

while received < total_size:
    chunk = socket.recv(4096)
    received += len(chunk)
    print_progress(received, total_size)
```

## JSON Functions

### `is_valid_json(data)`
Check if string is valid JSON.

**Parameters:**
- `data` (str): String to validate

**Returns:** bool - True if valid JSON

**Example:**
```python
from kn_sock.utils import is_valid_json

if is_valid_json(received_data):
    data = json.loads(received_data)
else:
    print("Invalid JSON received")
```
