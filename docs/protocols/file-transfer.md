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

## Related Topics

- **[TCP Protocol](tcp.md)** - For reliable JSON communication
- **[UDP Protocol](udp.md)** - For fast JSON messaging
- **[File Transfer](file-transfer.md)** - For large data transfer
- **[API Reference](../api-reference.md)** - Complete function documentation 