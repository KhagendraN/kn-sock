# File Transfer

kn-sock provides robust file transfer capabilities over TCP, supporting both synchronous and asynchronous operations with progress tracking.

## Overview

File transfer features in kn-sock:
- Reliable file transmission over TCP
- Progress tracking with visual progress bars
- Support for large files
- Both synchronous and asynchronous operations
- Automatic file metadata handling
- Error handling and recovery

## Basic File Transfer

### File Server

```python
from kn_sock import start_file_server

# Start a file server that saves received files to /path/to/save/directory
start_file_server(8080, "/path/to/save/directory")
```

### File Client

```python
from kn_sock import send_file

# Send a file to the server
send_file("localhost", 8080, "path/to/your/file.txt")
```

### File Server with Custom Handler

```python
from kn_sock import start_file_server

def file_received_handler(filename, filepath, addr):
    """Called when a file is successfully received"""
    print(f"File '{filename}' received from {addr} and saved to {filepath}")

start_file_server(8080, "/path/to/save/directory", handler=file_received_handler)
```

## Asynchronous File Transfer

### Async File Server

```python
import asyncio
from kn_sock import start_file_server_async

async def main():
    await start_file_server_async(8080, "/path/to/save/directory")

asyncio.run(main())
```

### Async File Client

```python
import asyncio
from kn_sock import send_file_async

async def main():
    await send_file_async("localhost", 8080, "path/to/your/file.txt")

asyncio.run(main())
```

## Progress Tracking

All file transfer functions support progress bars using tqdm:

### Enable Progress Bar

```python
from kn_sock import send_file

# Show progress bar (default if tqdm is installed)
send_file('localhost', 8080, 'file.txt', show_progress=True)
```

### Disable Progress Bar

```python
from kn_sock import send_file

# Disable progress bar
send_file('localhost', 8080, 'file.txt', show_progress=False)
```

### Custom Progress Callback

```python
from kn_sock import send_file

def progress_callback(bytes_sent, total_bytes, filename):
    percentage = (bytes_sent / total_bytes) * 100
    print(f"Sending {filename}: {percentage:.1f}% complete")

send_file('localhost', 8080, 'file.txt', progress_callback=progress_callback)
```

## Advanced File Transfer

### Multiple File Transfer

```python
import os
from kn_sock import send_file

def send_directory(host, port, directory_path):
    """Send all files in a directory"""
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            print(f"Sending {filename}...")
            send_file(host, port, filepath)

# Send all files in a directory
send_directory("localhost", 8080, "/path/to/directory")
```

### Selective File Transfer

```python
import os
from kn_sock import send_file

def send_files_by_extension(host, port, directory_path, extensions):
    """Send files with specific extensions"""
    for filename in os.listdir(directory_path):
        if any(filename.endswith(ext) for ext in extensions):
            filepath = os.path.join(directory_path, filename)
            if os.path.isfile(filepath):
                print(f"Sending {filename}...")
                send_file(host, port, filepath)

# Send only image files
send_files_by_extension("localhost", 8080, "/path/to/directory", ['.jpg', '.png', '.gif'])
```

### File Transfer with Metadata

```python
import os
import json
from kn_sock import send_json, send_file

def send_file_with_metadata(host, port, filepath):
    """Send file metadata first, then the file"""
    filename = os.path.basename(filepath)
    file_size = os.path.getsize(filepath)
    file_modified = os.path.getmtime(filepath)
    
    # Send metadata
    metadata = {
        "filename": filename,
        "size": file_size,
        "modified": file_modified,
        "type": "file_transfer"
    }
    send_json(host, port, metadata)
    
    # Send the actual file
    send_file(host, port, filepath)

send_file_with_metadata("localhost", 8080, "document.pdf")
```

## Error Handling

### File Transfer Errors

```python
from kn_sock.errors import FileTransferError, ConnectionTimeoutError

try:
    send_file("localhost", 8080, "large_file.zip")
except FileTransferError as e:
    print(f"File transfer failed: {e}")
except ConnectionTimeoutError:
    print("Connection timed out during file transfer")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Server-side Error Handling

```python
from kn_sock import start_file_server
import os

def handle_file_error(error, addr):
    """Handle file transfer errors"""
    print(f"Error receiving file from {addr}: {error}")

def validate_file(filename, filepath):
    """Validate received files"""
    # Check file size
    if os.path.getsize(filepath) > 100 * 1024 * 1024:  # 100MB limit
        raise ValueError("File too large")
    
    # Check file extension
    allowed_extensions = ['.txt', '.pdf', '.jpg', '.png']
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise ValueError("File type not allowed")

start_file_server(
    8080, 
    "/path/to/save/directory",
    error_handler=handle_file_error,
    validator=validate_file
)
```

## Performance Optimization

### Chunked Transfer

For very large files, consider chunked transfer:

```python
from kn_sock.utils import chunked_file_reader
from kn_sock import send_tcp_bytes

def send_large_file_chunked(host, port, filepath, chunk_size=1024*1024):
    """Send large file in chunks"""
    filename = os.path.basename(filepath)
    
    # Send file info
    file_info = {
        "filename": filename,
        "size": os.path.getsize(filepath),
        "chunk_size": chunk_size
    }
    send_json(host, port, file_info)
    
    # Send file in chunks
    for chunk in chunked_file_reader(filepath, chunk_size):
        send_tcp_bytes(host, port, chunk)
```

### Compression

For bandwidth optimization, use compression:

```python
from kn_sock.compression import compress_data
import gzip

def send_compressed_file(host, port, filepath):
    """Send compressed file"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    compressed_data = gzip.compress(data)
    send_tcp_bytes(host, port, compressed_data)
```

## Use Cases

### Backup System

```python
import schedule
import time
from kn_sock import send_file

def backup_files():
    """Daily backup of important files"""
    files_to_backup = [
        "/path/to/database.sql",
        "/path/to/config.json",
        "/path/to/logs/"
    ]
    
    for filepath in files_to_backup:
        try:
            send_file("backup-server", 8080, filepath)
            print(f"Backed up {filepath}")
        except Exception as e:
            print(f"Failed to backup {filepath}: {e}")

# Schedule daily backup at 2 AM
schedule.every().day.at("02:00").do(backup_files)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Log File Transfer

```python
import os
from datetime import datetime
from kn_sock import send_file

def transfer_logs():
    """Transfer log files older than 1 day"""
    log_directory = "/var/log/myapp"
    cutoff_time = datetime.now().timestamp() - 86400  # 24 hours ago
    
    for filename in os.listdir(log_directory):
        filepath = os.path.join(log_directory, filename)
        if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff_time:
            try:
                send_file("log-server", 8080, filepath)
                print(f"Transferred log file: {filename}")
            except Exception as e:
                print(f"Failed to transfer {filename}: {e}")
```

### Media File Distribution

```python
import os
from kn_sock import send_file

def distribute_media_files(host, port, media_directory):
    """Distribute media files to multiple servers"""
    media_extensions = ['.mp4', '.avi', '.mkv', '.mp3', '.wav']
    
    for filename in os.listdir(media_directory):
        if any(filename.endswith(ext) for ext in media_extensions):
            filepath = os.path.join(media_directory, filename)
            if os.path.isfile(filepath):
                print(f"Distributing {filename}...")
                send_file(host, port, filepath, show_progress=True)

# Distribute to multiple servers
servers = [
    ("server1", 8080),
    ("server2", 8080),
    ("server3", 8080)
]

for host, port in servers:
    distribute_media_files(host, port, "/path/to/media")
```

## CLI Usage

```bash
# Start a file server
kn-sock run-file-server 8080 /path/to/save/directory

# Send a file
kn-sock send-file localhost 8080 path/to/your/file.txt

# Send file with progress
kn-sock send-file localhost 8080 large_file.zip --show-progress
```

## Best Practices

1. **Use progress tracking**: Enable progress bars for large files
2. **Handle errors gracefully**: Implement proper error handling
3. **Validate files**: Check file size and type on the server side
4. **Use compression**: For large files or slow connections
5. **Implement retry logic**: For unreliable network connections
6. **Monitor disk space**: Ensure sufficient space on the receiving server
7. **Use appropriate chunk sizes**: Balance memory usage and performance

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `show_progress` | Show progress bar | True (if tqdm installed) |
| `progress_callback` | Custom progress function | None |
| `chunk_size` | Bytes per chunk | 4096 |
| `timeout` | Transfer timeout | 30 seconds |

## Related Topics

- **[TCP Protocol](tcp.md)** - For reliable file transfer
- **[JSON Communication](json.md)** - For file metadata exchange
- **[Compression](../advanced/compression.md)** - For optimizing transfer size
- **[API Reference](../api-reference.md)** - Complete function documentation 