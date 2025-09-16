# Troubleshooting Guide

This guide provides solutions to common issues you may encounter while using kn-sock.

## General Issues

### Port Conflicts

**Error:** `OSError: [Errno 98] Address already in use`

**Cause:** The port is already used by another process.

**Solutions:**
1. Use a different port number:
   ```python
   start_tcp_server(8081, handler)  # Instead of 8080
   ```

2. Find and stop the process using the port:
   ```bash
   # Find the process
   lsof -i :8080
   # or
   netstat -tuln | grep 8080
   
   # Kill the process (replace PID with actual process ID)
   sudo kill <PID>
   ```

3. Wait for the port to be released (usually takes a few seconds after stopping a server).

### Permission Issues

**Error:** `PermissionError: [Errno 13] Permission denied`

**Cause:** Insufficient permissions to bind to the port.

**Solutions:**
1. Use a port number above 1024 (ports below 1024 require root privileges):
   ```python
   start_tcp_server(8080, handler)  # Instead of 80
   ```

2. Run with appropriate permissions (not recommended for production):
   ```bash
   sudo python your_script.py
   ```

### Network Connectivity

**Error:** `ConnectionRefusedError` or `TimeoutError`

**Cause:** Server not running, wrong address/port, or network issues.

**Solutions:**
1. Verify server is running:
   ```python
   # Check if server is actually listening
   import socket
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   result = sock.connect_ex(('localhost', 8080))
   if result == 0:
       print("Port is open")
   else:
       print("Port is closed")
   sock.close()
   ```

2. Check firewall settings:
   ```bash
   # Temporarily disable firewall for testing
   sudo ufw disable  # Ubuntu/Debian
   sudo systemctl stop firewalld  # CentOS/RHEL
   ```

3. Use correct host/port:
   ```python
   # Make sure host and port match between client and server
   send_tcp_message("localhost", 8080, "Hello")  # Not 127.0.0.1:8081
   ```

## TCP/UDP Issues

### Connection Timeout

**Error:** `ConnectionTimeoutError`

**Cause:** Network latency or server overload.

**Solutions:**
1. Increase timeout:
   ```python
   import socket
   socket.setdefaulttimeout(30)  # 30 seconds
   ```

2. Implement retry logic:
   ```python
   from kn_sock.decorators import retry
   
   @retry(retries=3, delay=1.0)
   def send_with_retry(host, port, message):
       send_tcp_message(host, port, message)
   ```

### Data Corruption

**Error:** Unexpected data received

**Cause:** Network issues or encoding problems.

**Solutions:**
1. Use proper encoding:
   ```python
   # Server
   def handler(data, addr, client_socket):
       message = data.decode('utf-8')  # Specify encoding
       print(f"Received: {message}")
   
   # Client
   send_tcp_message("localhost", 8080, "Hello".encode('utf-8'))
   ```

2. Implement data validation:
   ```python
   def validate_data(data):
       try:
           decoded = data.decode('utf-8')
           return decoded
       except UnicodeDecodeError:
           print("Invalid data received")
           return None
   ```

## SSL/TLS Issues

### Certificate Verification Failed

**Error:** `ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]`

**Cause:** Invalid, missing, or self-signed certificates.

**Solutions:**
1. For testing, disable verification:
   ```python
   send_ssl_tcp_message("localhost", 8443, "Hello", verify=False)
   ```

2. Provide correct certificates:
   ```python
   send_ssl_tcp_message(
       "localhost", 8443, "Hello",
       cafile="ca.crt",
       certfile="client.crt",
       keyfile="client.key"
   )
   ```

3. Generate proper certificates:
   ```bash
   # Generate self-signed certificate for testing
   openssl req -new -x509 -keyout server.key -out server.crt -days 365 -nodes
   ```

### Certificate File Not Found

**Error:** `FileNotFoundError: [Errno 2] No such file or directory`

**Cause:** Certificate files don't exist or wrong path.

**Solutions:**
1. Check file paths:
   ```python
   import os
   certfile = "server.crt"
   if not os.path.exists(certfile):
       print(f"Certificate file {certfile} not found")
   ```

2. Use absolute paths:
   ```python
   certfile = "/path/to/server.crt"
   keyfile = "/path/to/server.key"
   ```

## File Transfer Issues

### File Not Found

**Error:** `FileNotFoundError: [Errno 2] No such file or directory`

**Cause:** File doesn't exist or wrong path.

**Solutions:**
1. Check file existence:
   ```python
   import os
   if os.path.exists(filepath):
       send_file("localhost", 8080, filepath)
   else:
       print(f"File {filepath} not found")
   ```

2. Use absolute paths:
   ```python
   filepath = os.path.abspath("file.txt")
   send_file("localhost", 8080, filepath)
   ```

### Incomplete File Transfer

**Error:** File received but corrupted or incomplete

**Cause:** Network interruption or insufficient disk space.

**Solutions:**
1. Check disk space:
   ```python
   import shutil
   total, used, free = shutil.disk_usage("/path/to/save/directory")
   print(f"Free space: {free // (1024**3)} GB")
   ```

2. Implement retry logic:
   ```python
   @retry(retries=3, delay=2.0)
   def send_file_with_retry(host, port, filepath):
       send_file(host, port, filepath)
   ```

3. Verify file integrity:
   ```python
   import hashlib
   
   def get_file_hash(filepath):
       with open(filepath, 'rb') as f:
           return hashlib.md5(f.read()).hexdigest()
   
   # Before sending
   original_hash = get_file_hash(filepath)
   
   # After receiving, verify hash matches
   ```

## Video/Audio Issues

### PyAudio Errors

**Error:** `OSError: [Errno -9996] Invalid input device`

**Cause:** Audio device not available or misconfigured.

**Solutions:**
1. Install audio drivers:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install portaudio19-dev
   
   # Arch Linux
   sudo pacman -S pulseaudio pulseaudio-alsa
   
   # macOS
   brew install portaudio
   ```

2. Set audio environment variables:
   ```bash
   export PULSE_SERVER=unix:/tmp/pulse-socket
   export ALSA_PCM_CARD=0
   ```

3. Use audio-only client:
   ```bash
   python examples/video_chat_client_no_audio.py 127.0.0.1 myroom alice
   ```

### OpenCV Camera Issues

**Error:** `cv2.error: OpenCV(4.x.x) /path/to/cap.cpp: error: (-215:Assertion failed)`

**Cause:** Camera not available or in use.

**Solutions:**
1. Check camera permissions:
   ```bash
   # Linux
   ls -l /dev/video*
   sudo usermod -a -G video $USER
   ```

2. Test camera separately:
   ```python
   import cv2
   cap = cv2.VideoCapture(0)
   if cap.isOpened():
       print("Camera is working")
       cap.release()
   else:
       print("Camera not available")
   ```

3. Try different camera indices:
   ```python
   # Try different camera numbers
   for i in range(5):
       cap = cv2.VideoCapture(i)
       if cap.isOpened():
           print(f"Camera {i} is available")
           cap.release()
           break
   ```

### Display Issues

**Error:** `cv2.error: OpenCV(4.x.x) /path/to/window.cpp: error: (-215:Assertion failed)`

**Cause:** Display backend issues.

**Solutions:**
1. Set display backend:
   ```bash
   export QT_QPA_PLATFORM=xcb
   export DISPLAY=:0
   ```

2. Use headless mode:
   ```python
   import os
   os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
   ```

## JSON Communication Issues

### Invalid JSON

**Error:** `InvalidJSONError` or `json.JSONDecodeError`

**Cause:** Malformed JSON data.

**Solutions:**
1. Validate JSON before sending:
   ```python
   import json
   
   def send_valid_json(host, port, data):
       try:
           json.dumps(data)  # Validate JSON
           send_json(host, port, data)
       except TypeError as e:
           print(f"Invalid JSON data: {e}")
   ```

2. Use JSON decorator:
   ```python
   from kn_sock.decorators import ensure_json_input
   
   @ensure_json_input
   def handle_json_message(data, addr, client_socket):
       # data is guaranteed to be valid JSON
       pass
   ```

### Encoding Issues

**Error:** Unicode encoding/decoding errors

**Cause:** Character encoding mismatches.

**Solutions:**
1. Use UTF-8 encoding:
   ```python
   # Server
   def handler(data, addr, client_socket):
       try:
           message = data.decode('utf-8')
           json_data = json.loads(message)
       except UnicodeDecodeError:
           print("Invalid encoding")
   ```

2. Handle encoding explicitly:
   ```python
   # Client
   json_str = json.dumps(data, ensure_ascii=False)
   send_tcp_message(host, port, json_str.encode('utf-8'))
   ```

## WebSocket Issues

### Connection Failed

**Error:** `WebSocket connection failed`

**Cause:** Server not running or protocol mismatch.

**Solutions:**
1. Verify server is running:
   ```python
   # Test basic connectivity first
   import socket
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   result = sock.connect_ex(('localhost', 8765))
   sock.close()
   ```

2. Check WebSocket handshake:
   ```python
   # Use proper WebSocket client
   ws = connect_websocket("localhost", 8765)
   if ws.open:
       print("WebSocket connected successfully")
   ```

### Message Format Issues

**Error:** WebSocket messages not received

**Cause:** Incorrect message format or protocol.

**Solutions:**
1. Use proper WebSocket methods:
   ```python
   # Send text message
   ws.send("Hello WebSocket")
   
   # Receive message
   message = ws.recv()
   ```

2. Handle connection state:
   ```python
   if ws.open:
       ws.send(message)
   else:
       print("WebSocket not connected")
   ```

## Performance Issues

### High Memory Usage

**Cause:** Large buffers or memory leaks.

**Solutions:**
1. Use smaller buffers:
   ```python
   # For file transfer
   send_file(host, port, filepath, chunk_size=1024)
   ```

2. Implement streaming:
   ```python
   from kn_sock.utils import chunked_file_reader
   
   for chunk in chunked_file_reader(filepath, chunk_size=4096):
       # Process chunk
       pass
   ```

### Slow Performance

**Cause:** Network latency or inefficient code.

**Solutions:**
1. Use connection pooling:
   ```python
   from kn_sock import TCPConnectionPool
   
   pool = TCPConnectionPool('localhost', 8080, max_size=5)
   with pool.connection() as conn:
       conn.sendall(b"Hello")
   ```

2. Use async operations:
   ```python
   import asyncio
   from kn_sock import send_tcp_message_async
   
   asyncio.run(send_tcp_message_async("localhost", 8080, "Hello"))
   ```

## Debugging Tips

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use kn-sock CLI with verbose flag
# kn-sock --verbose run-tcp-server 8080
```

### Test Network Connectivity

```python
def test_connectivity(host, port):
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False
```

### Monitor System Resources

```bash
# Monitor network connections
netstat -tuln

# Monitor process resources
top -p $(pgrep -f "python.*kn-sock")

# Monitor disk usage
df -h
```

## Getting Help

### Check Documentation

- Review the [API Reference](api-reference.md) for function details
- Check [Getting Started](getting-started.md) for basic usage
- Look at [examples](../examples/) for working code samples

### Report Issues

When reporting issues, include:

1. **Environment details:**
   - Operating system and version
   - Python version
   - kn-sock version

2. **Error details:**
   - Complete error message and traceback
   - Steps to reproduce the issue
   - Expected vs actual behavior

3. **Code example:**
   - Minimal code that reproduces the issue
   - Any relevant configuration

4. **System information:**
   - Network configuration
   - Firewall settings
   - Available ports

### Common Error Messages

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `Address already in use` | Port conflict | Use different port or kill existing process |
| `Connection refused` | Server not running | Start server first |
| `Permission denied` | Insufficient privileges | Use port > 1024 or run with sudo |
| `Timeout` | Network issues | Increase timeout or check connectivity |
| `Invalid JSON` | Malformed data | Validate JSON before sending |
| `SSL certificate failed` | Certificate issues | Use correct certs or disable verification |
| `File not found` | Wrong path | Check file existence and path |
| `Camera not available` | Hardware/permission issues | Check camera permissions and availability |

## Related Topics

- **[Getting Started](getting-started.md)** - For basic setup and usage
- **[API Reference](api-reference.md)** - For detailed function documentation
- **[CLI Guide](cli.md)** - For command-line troubleshooting 