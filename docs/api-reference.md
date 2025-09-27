# API Reference

This page provides a comprehensive reference for all public functions and classes in kn-sock.

## TCP Functions

### Server Functions

#### `start_tcp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)`

Start a synchronous TCP server.

**Parameters:**
- `port` (int): Port to bind.
- `handler_func` (callable): Function called for each client (data, addr, client_socket).
- `host` (str): Host to bind (default: '0.0.0.0').
- `shutdown_event` (threading.Event, optional): For graceful shutdown.

**Returns:** None

#### `start_threaded_tcp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)`

Start a threaded TCP server for handling multiple clients concurrently.

**Parameters:** Same as `start_tcp_server`

**Returns:** None

#### `start_async_tcp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)`

Start an async TCP server.

**Parameters:**
- `port` (int): Port to bind.
- `handler_func` (async callable): Async function called for each client (data, addr, writer).
- `host` (str): Host to bind (default: '0.0.0.0').
- `shutdown_event` (asyncio.Event, optional): For graceful shutdown.

**Returns:** None

### Client Functions

#### `send_tcp_message(host, port, message)`

Send a string message over TCP.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port.
- `message` (str): Message to send.

**Returns:** None

#### `send_tcp_bytes(host, port, data)`

Send raw bytes over TCP.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port.
- `data` (bytes): Data to send.

**Returns:** None

#### `send_tcp_message_async(host, port, message)`

Send a string message over TCP asynchronously.

**Parameters:** Same as `send_tcp_message`

**Returns:** None

## Secure TCP (SSL/TLS) Functions

### Server Functions

#### `start_ssl_tcp_server(port, handler_func, certfile, keyfile, cafile=None, require_client_cert=False, host='0.0.0.0', shutdown_event=None)`

Start a secure SSL/TLS TCP server.

**Parameters:**
- `port` (int): Port to bind.
- `handler_func` (callable): Function called for each client (data, addr, client_socket).
- `certfile` (str): Path to server certificate (PEM).
- `keyfile` (str): Path to private key (PEM).
- `cafile` (str, optional): CA cert for client verification.
- `require_client_cert` (bool): Require client cert (mutual TLS).
- `host` (str): Host to bind (default: '0.0.0.0').
- `shutdown_event` (threading.Event, optional): For graceful shutdown.

**Returns:** None

#### `start_async_ssl_tcp_server(port, handler_func, certfile, keyfile, cafile=None, require_client_cert=False, host='0.0.0.0', shutdown_event=None)`

Start an async secure SSL/TLS TCP server.

**Parameters:** Same as `start_ssl_tcp_server` but handler is async.

**Returns:** None

### Client Functions

#### `send_ssl_tcp_message(host, port, message, cafile=None, certfile=None, keyfile=None, verify=True)`

Send a message over SSL/TLS TCP.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port.
- `message` (str): Message to send.
- `cafile` (str, optional): CA cert for server verification.
- `certfile` (str, optional): Client certificate.
- `keyfile` (str, optional): Client private key.
- `verify` (bool): Verify server cert (default: True).

**Returns:** None

#### `send_ssl_tcp_message_async(host, port, message, cafile=None, certfile=None, keyfile=None, verify=True)`

Send a message over SSL/TLS TCP asynchronously.

**Parameters:** Same as `send_ssl_tcp_message`

**Returns:** None

## UDP Functions

### Server Functions

#### `start_udp_server(port, handler_func, host='0.0.0.0', shutdown_event=None)`

Start a synchronous UDP server.

**Parameters:**
- `port` (int): Port to bind.
- `handler_func` (callable): Function called for each message (data, addr, server_socket).
- `host` (str): Host to bind (default: '0.0.0.0').
- `shutdown_event` (threading.Event, optional): For graceful shutdown.

**Returns:** None

#### `start_udp_server_async(port, handler_func, host='0.0.0.0', shutdown_event=None)`

Start an async UDP server.

**Parameters:** Same as `start_udp_server` but handler is async.

**Returns:** None

### Client Functions

#### `send_udp_message(host, port, message)`

Send a string message over UDP.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port.
- `message` (str): Message to send.

**Returns:** None

#### `send_udp_message_async(host, port, message)`

Send a string message over UDP asynchronously.

**Parameters:** Same as `send_udp_message`

**Returns:** None

#### `send_udp_multicast(group, port, message, ttl=1)`

Send a message to a UDP multicast group.

**Parameters:**
- `group` (str): Multicast group address.
- `port` (int): Target port.
- `message` (str): Message to send.
- `ttl` (int): Time-to-live for multicast packets.

**Returns:** None

#### `start_udp_multicast_server(group, port, handler_func, listen_ip='0.0.0.0', shutdown_event=None)`

Start a UDP multicast server.

**Parameters:**
- `group` (str): Multicast group address.
- `port` (int): Port to bind.
- `handler_func` (callable): Function called for each message.
- `listen_ip` (str): IP to listen on for multicast.
- `shutdown_event` (threading.Event, optional): For graceful shutdown.

**Returns:** None

## File Transfer Functions

### Server Functions

#### `start_file_server(port, save_dir, host='0.0.0.0')`

Start a TCP file receiver.

**Parameters:**
- `port` (int): Port to bind.
- `save_dir` (str): Directory to save received files.
- `host` (str): Host to bind (default: '0.0.0.0').

**Returns:** None

#### `start_file_server_async(port, save_dir, host='0.0.0.0')`

Start an async TCP file receiver.

**Parameters:** Same as `start_file_server`

**Returns:** None

### Client Functions

#### `send_file(host, port, filepath, show_progress=True, progress_callback=None)`

Send a file over TCP.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port.
- `filepath` (str): Path to file to send.
- `show_progress` (bool): Show progress bar (default: True).
- `progress_callback` (callable, optional): Custom progress function.

**Returns:** None

#### `send_file_async(host, port, filepath)`

Send a file over TCP asynchronously.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port.
- `filepath` (str): Path to file to send.

**Returns:** None

## JSON Socket Functions

### Server Functions

#### `start_json_server(port, handler_func, host='0.0.0.0')`

Start a JSON-over-TCP server.

**Parameters:**
- `port` (int): Port to bind.
- `handler_func` (callable): Function called for each message (data: dict, addr, client_socket).
- `host` (str): Host to bind (default: '0.0.0.0').

**Returns:** None

#### `start_json_server_async(port, handler_func, host='0.0.0.0')`

Start an async JSON-over-TCP server.

**Parameters:** Same as `start_json_server` but handler is async.

**Returns:** None

### Client Functions

#### `send_json(host, port, obj, timeout=5)`

Send a JSON object over TCP.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port.
- `obj` (dict): JSON-serializable object.
- `timeout` (int): Timeout in seconds.

**Returns:** None

#### `send_json_async(host, port, obj)`

Send a JSON object over TCP asynchronously.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port.
- `obj` (dict): JSON-serializable object.

**Returns:** None

### Response Helpers

#### `send_json_response(sock, data)`

Send a JSON response to a client.

**Parameters:**
- `sock` (socket.socket): Client socket.
- `data` (dict): JSON-serializable object.

**Returns:** None

#### `send_json_response_async(writer, data)`

Send a JSON response to a client asynchronously.

**Parameters:**
- `writer` (asyncio.StreamWriter): Writer object.
- `data` (dict): JSON-serializable object.

**Returns:** None

## WebSocket Functions

### Server Functions

#### `start_websocket_server(host, port, handler, shutdown_event=None)`

Start a WebSocket server.

**Parameters:**
- `host` (str): Host to bind.
- `port` (int): Port to bind.
- `handler` (callable): Function called for each client (ws).
- `shutdown_event` (threading.Event, optional): For graceful shutdown.

**Returns:** None

### Client Functions

#### `connect_websocket(host, port, resource='/', headers=None)`

Connect to a WebSocket server.

**Parameters:**
- `host` (str): Server host.
- `port` (int): Server port.
- `resource` (str): WebSocket resource path.
- `headers` (dict, optional): Extra headers.

**Returns:** WebSocket client object

#### `async_connect_websocket(host, port, resource='/', headers=None)`

Connect to a WebSocket server asynchronously.

**Parameters:** Same as `connect_websocket`

**Returns:** AsyncWebSocketConnection

## HTTP/HTTPS Functions

### Client Functions

#### `http_get(host, port=80, path='/', headers=None)`

Send an HTTP GET request.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port (default: 80).
- `path` (str): URL path.
- `headers` (dict): HTTP headers.

**Returns:** Response body (str)

#### `http_post(host, port=80, path='/', data='', headers=None)`

Send an HTTP POST request.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port (default: 80).
- `path` (str): URL path.
- `data` (str): POST data.
- `headers` (dict): HTTP headers.

**Returns:** Response body (str)

#### `https_get(host, port=443, path='/', headers=None, cafile=None)`

Send an HTTPS GET request.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port (default: 443).
- `path` (str): URL path.
- `headers` (dict): HTTP headers.
- `cafile` (str): CA cert for verification.

**Returns:** Response body (str)

#### `https_post(host, port=443, path='/', data='', headers=None, cafile=None)`

Send an HTTPS POST request.

**Parameters:**
- `host` (str): Target host.
- `port` (int): Target port (default: 443).
- `path` (str): URL path.
- `data` (str): POST data.
- `headers` (dict): HTTP headers.
- `cafile` (str): CA cert for verification.

**Returns:** Response body (str)

### Server Functions

#### `start_http_server(host, port, static_dir=None, routes=None, shutdown_event=None)`

Start an HTTP server.

**Parameters:**
- `host` (str): Host to bind.
- `port` (int): Port to bind.
- `static_dir` (str, optional): Directory to serve files from.
- `routes` (dict, optional): Dict mapping (method, path) to handler functions.
- `shutdown_event` (threading.Event, optional): For graceful shutdown.

**Returns:** None

## Pub/Sub Functions

### Server Functions

#### `start_pubsub_server(port, handler_func=None, host='0.0.0.0', shutdown_event=None)`

Start a TCP pub/sub server for topic-based message distribution.

**Parameters:**
- `port` (int): Port to bind the server to.
- `handler_func` (callable, optional): Custom handler for processing messages. Called with `(data, client_sock, server)` where `data` is the parsed JSON message, `client_sock` is the client socket, and `server` is the PubSubServer instance.
- `host` (str): Host address to bind to (default: '0.0.0.0').
- `shutdown_event` (threading.Event, optional): Event for graceful shutdown.

**Returns:** None

**Handler Function Signature:**
```python
def custom_handler(data, client_sock, server):
    """
    Args:
        data (dict): Parsed JSON message from client
        client_sock (socket.socket): Client socket connection
        server (PubSubServer): Server instance
    """
    pass
```

**Example:**
```python
from kn_sock import start_pubsub_server

def message_handler(data, client_sock, server):
    action = data.get("action")
    if action == "publish":
        print(f"Message: {data.get('message')}")

start_pubsub_server(8080, message_handler)
```

### Client Class

#### `PubSubClient(host, port)`

Create a PubSub client for publishing and subscribing to topics.

**Parameters:**
- `host` (str): Server hostname or IP address.
- `port` (int): Server port number.

**Methods:**

##### `subscribe(topic: str) -> None`
Subscribe to a topic to receive messages published to it.

**Parameters:**
- `topic` (str): Topic name to subscribe to.

##### `unsubscribe(topic: str) -> None`
Unsubscribe from a topic to stop receiving its messages.

**Parameters:**
- `topic` (str): Topic name to unsubscribe from.

##### `publish(topic: str, message: str) -> None`
Publish a message to a topic for distribution to subscribers.

**Parameters:**
- `topic` (str): Topic name to publish to.
- `message` (str): Message content to publish.

##### `recv(timeout: float = None) -> Optional[dict]`
Receive a message from subscribed topics.

**Parameters:**
- `timeout` (float, optional): Timeout in seconds. None for blocking receive.

**Returns:** Dictionary with 'topic' and 'message' keys, or None if timeout.

##### `close() -> None`
Close the client connection and cleanup resources.

**Example:**
```python
from kn_sock import PubSubClient

# Publisher
client = PubSubClient("localhost", 8080)
client.publish("news", "Breaking news!")
client.close()

# Subscriber
client = PubSubClient("localhost", 8080)
client.subscribe("news")
message = client.recv(timeout=5.0)
if message:
    print(f"Received: {message['message']}")
client.close()
```

## RPC Functions

### Server Functions

#### `start_rpc_server(port, register_funcs, host='0.0.0.0', shutdown_event=None)`

Start an RPC server.

**Parameters:**
- `port` (int): Port to bind.
- `register_funcs` (dict): Function name to callable mapping.
- `host` (str): Host to bind (default: '0.0.0.0').
- `shutdown_event` (threading.Event, optional): For graceful shutdown.

**Returns:** None

### Client Class

#### `RPCClient(host, port)`

RPC client class.

**Methods:**
- `call(function, *args, **kwargs)`: Call a remote function.
- `close()`: Close the connection.

## Live Streaming Functions

### Server Functions

#### `start_live_stream(port, video_paths, host='0.0.0.0', audio_port=None)`

Start a live video/audio stream server.

**Parameters:**
- `port` (int): Video port.
- `video_paths` (list of str): Video file paths.
- `host` (str): Host to bind (default: '0.0.0.0').
- `audio_port` (int, optional): Audio port.

**Returns:** None

### Client Functions

#### `connect_to_live_server(ip, port, audio_port=None)`

Connect to a live stream server.

**Parameters:**
- `ip` (str): Server IP.
- `port` (int): Video port.
- `audio_port` (int, optional): Audio port.

**Returns:** None

### Classes

#### `LiveStreamServer(video_paths, host='0.0.0.0', video_port=9000, audio_port=9001, control_port=9010)`

Live stream server class.

**Methods:**
- `start()`: Start the server.

#### `LiveStreamClient(host, video_port=9000, audio_port=9001, control_port=9010, video_buffer_ms=200, audio_buffer_ms=100, video_fps=30)`

Live stream client class.

**Methods:**
- `start()`: Start the client.

## Video Chat Functions

### Classes

#### `VideoChatServer(host='0.0.0.0', video_port=9000, audio_port=9001, text_port=9002)`

Multi-client video chat server class.

**Methods:**
- `start()`: Start the server.

#### `VideoChatClient(server_ip, video_port=9000, audio_port=9001, text_port=9002, room='default', nickname='user')`

Video chat client class.

**Methods:**
- `start()`: Start the client.
- `send_message(message)`: Send a text message.
- `mute()`: Mute microphone.
- `unmute()`: Unmute microphone.
- `toggle_video()`: Toggle video on/off.

## Connection Pooling

### Classes

#### `TCPConnectionPool(host, port, max_size=10, idle_timeout=60, ssl=False, **ssl_kwargs)`

TCP connection pool for efficient connection reuse.

**Methods:**
- `connection()`: Get a connection from the pool.
- `closeall()`: Close all connections in the pool.

## Utilities

### Network Utilities

#### `get_free_port()`

Find a free TCP port.

**Returns:** int

#### `get_local_ip()`

Get the local IP address.

**Returns:** str

### File Utilities

#### `chunked_file_reader(filepath, chunk_size=4096)`

Yield file data in chunks.

**Parameters:**
- `filepath` (str): Path to file.
- `chunk_size` (int): Bytes per chunk.

**Returns:** Iterator[bytes]

#### `recv_all(sock, total_bytes)`

Receive exactly `total_bytes` from a socket.

**Parameters:**
- `sock` (socket.socket): Socket.
- `total_bytes` (int): Number of bytes to receive.

**Returns:** bytes

### Progress Display

#### `print_progress(received_bytes, total_bytes)`

Print file transfer progress.

**Parameters:**
- `received_bytes` (int): Bytes received.
- `total_bytes` (int): Total bytes.

**Returns:** None

### JSON Utility

#### `is_valid_json(json_string)`

Check if a string is valid JSON.

**Parameters:**
- `json_string` (str): String to check.

**Returns:** bool

## Decorators

### `log_exceptions(raise_error=False)`

Logs exceptions and optionally re-raises them.

**Parameters:**
- `raise_error` (bool): Whether to re-raise the exception.

### `retry(retries=3, delay=1.0, exceptions=(Exception,))`

Retries a function upon failure.

**Parameters:**
- `retries` (int): Number of retry attempts.
- `delay` (float): Delay between attempts in seconds.
- `exceptions` (tuple): Exception types to catch.

### `measure_time`

Measures and prints the execution time of the wrapped function.

### `ensure_json_input`

Validates that the first argument is a valid JSON object.

## Errors

### Base Exception

#### `EasySocketError`

Base exception for all kn_sock errors.

### Connection Errors

#### `ConnectionTimeoutError`

Raised when a connection or read/write operation times out.

#### `PortInUseError`

Raised when a specified port is already in use.

### Data & Protocol Errors

#### `InvalidJSONError`

Raised when a JSON message cannot be decoded.

#### `UnsupportedProtocolError`

Raised when a requested protocol is not supported.

### File Transfer Errors

#### `FileTransferError`

Raised when file transfer fails.

## Compression

### Functions

#### `compress_data(data, method='gzip')`

Compress data using gzip or deflate.

**Parameters:**
- `data` (bytes): Data to compress.
- `method` (str): Compression method ('gzip' or 'deflate').

**Returns:** bytes

#### `decompress_data(data)`

Decompress data (auto-detects gzip/deflate).

**Parameters:**
- `data` (bytes): Compressed data.

**Returns:** bytes

#### `detect_compression(data)`

Detect compression type.

**Parameters:**
- `data` (bytes): Data to analyze.

**Returns:** str ('gzip', 'deflate', or 'none')

## Message Queues

### Classes

#### `InMemoryQueue()`

Thread-safe FIFO queue for fast, in-memory message passing.

**Methods:**
- `put(item)`: Add item to queue.
- `get()`: Get item from queue.
- `task_done()`: Mark task as done.
- `join()`: Wait for all tasks to complete.
- `empty()`: Check if queue is empty.
- `qsize()`: Get queue size.

#### `FileQueue(filename)`

Persistent queue that stores messages on disk.

**Methods:** Same as InMemoryQueue plus:
- `close()`: Close the queue.

## Protocol Buffers

### Functions

#### `serialize_message(msg)`

Serialize a protobuf message to bytes.

**Parameters:**
- `msg`: Protobuf message object.

**Returns:** bytes

#### `deserialize_message(data, schema)`

Deserialize bytes to a protobuf message.

**Parameters:**
- `data` (bytes): Serialized data.
- `schema`: Protobuf message class.

**Returns:** Protobuf message object

## Load Balancing

### Classes

#### `RoundRobinLoadBalancer()`

Cycles through servers in order.

**Methods:**
- `add_server(server)`: Add a server.
- `remove_server(server)`: Remove a server.
- `get_server()`: Get next server in round-robin order.

#### `LeastConnectionsLoadBalancer()`

Selects server with fewest active connections.

**Methods:** Same as RoundRobinLoadBalancer plus:
- `update_connections(server, count)`: Update connection count for server.

## Interactive CLI

### Functions

#### `start_interactive_cli()`

Start the interactive command-line interface.

**Returns:** None

### Commands

- `connect <name> <host> <port>`: Connect to a server
- `list`: List all active connections
- `select <name>`: Set default connection
- `send <message>`: Send a message
- `receive`: Receive a message
- `bg_receive`: Toggle background receive mode
- `history`: Show message history
- `disconnect <name>`: Disconnect a connection
- `quit`/`exit`: Exit the CLI
- `help`: Show help

## Network Visibility Functions

> **⚠️ ETHICAL WARNING:** These functions are intended for use in authorized networks such as schools, labs, or controlled IT environments. Monitoring user traffic may be illegal without explicit consent. Use responsibly and ethically.

### ARP Scanning Functions

#### `arp_scan(network_range, interface=None, timeout=2, verbose=False)`

Perform ARP scan on a network range to discover active devices.

**Parameters:**
- `network_range` (str): Network range to scan (e.g., "192.168.1.0/24")
- `interface` (str, optional): Network interface to use (auto-detect if None)
- `timeout` (int): Timeout in seconds for each ARP request (default: 2)
- `verbose` (bool): Enable verbose logging (default: False)

**Returns:**
- `List[Dict[str, str]]`: List of dictionaries containing IP and MAC addresses of discovered devices

**Raises:**
- `ImportError`: If scapy is not available
- `ValueError`: If network range is invalid
- `RuntimeError`: If scanning fails

**Example:**
```python
from kn_sock.network import arp_scan

devices = arp_scan("192.168.1.0/24", verbose=True)
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}")
```

#### `arp_scan_simple(ip_range)`

Simple ARP scan that returns IP and MAC pairs.

**Parameters:**
- `ip_range` (str): IP range to scan (e.g., "192.168.1.0/24")

**Returns:**
- `List[Tuple[str, str]]`: List of tuples containing (IP, MAC) pairs

#### `get_local_network_info()`

Get information about the local network.

**Returns:**
- `Dict[str, str]`: Dictionary containing network information (local_ip, interface, gateway)

### MAC Address Lookup Functions

#### `mac_lookup(mac, use_api=True, api_key=None)`

Lookup MAC address vendor information.

**Parameters:**
- `mac` (str): MAC address to lookup
- `use_api` (bool): Whether to use online API (default: True)
- `api_key` (str, optional): Optional API key for online lookup

**Returns:**
- `Dict[str, str]`: Dictionary containing vendor information (mac, oui, vendor, source)

**Raises:**
- `ValueError`: If MAC address is invalid
- `requests.RequestException`: If API request fails

**Example:**
```python
from kn_sock.network import mac_lookup

result = mac_lookup("00:1A:2B:3C:4D:5E")
print(f"Vendor: {result['vendor']}")
```

#### `mac_lookup_api(mac, api_key=None)`

Lookup MAC address vendor using macvendors.co API.

**Parameters:**
- `mac` (str): MAC address to lookup
- `api_key` (str, optional): Optional API key for higher rate limits

**Returns:**
- `Dict[str, str]`: Dictionary containing vendor information

#### `mac_lookup_offline(mac)`

Lookup MAC address vendor using built-in OUI database.

**Parameters:**
- `mac` (str): MAC address to lookup

**Returns:**
- `Dict[str, str]`: Dictionary containing vendor information

#### `batch_mac_lookup(macs, use_api=True, api_key=None)`

Lookup multiple MAC addresses.

**Parameters:**
- `macs` (List[str]): List of MAC addresses to lookup
- `use_api` (bool): Whether to use online API
- `api_key` (str, optional): Optional API key for online lookup

**Returns:**
- `List[Dict[str, str]]`: List of dictionaries containing vendor information

#### `validate_mac(mac)`

Validate MAC address format.

**Parameters:**
- `mac` (str): MAC address to validate

**Returns:**
- `bool`: True if valid, False otherwise

### DNS Monitoring Functions

#### `monitor_dns(duration=60, interface=None, log_file=None, callback=None, verbose=False)`

Monitor DNS requests on the network.

**Parameters:**
- `duration` (int): Duration to monitor in seconds (default: 60)
- `interface` (str, optional): Network interface to monitor (auto-detect if None)
- `log_file` (str, optional): File to save DNS logs (JSON format)
- `callback` (callable, optional): Function to call for each DNS request
- `verbose` (bool): Enable verbose logging (default: False)

**Returns:**
- `List[Dict[str, Any]]`: List of DNS request records

**Raises:**
- `ImportError`: If scapy is not available
- `PermissionError`: If insufficient privileges
- `RuntimeError`: If monitoring fails

**Example:**
```python
from kn_sock.network import monitor_dns

results = monitor_dns(duration=60, log_file="dns_log.json", verbose=True)
for result in results:
    print(f"{result['source_ip']} -> {result['domain']}")
```

#### `monitor_dns_async(duration=60, interface=None, log_file=None, callback=None, verbose=False)`

Start DNS monitoring in a separate thread.

**Parameters:**
- `duration` (int): Duration to monitor in seconds
- `interface` (str, optional): Network interface to monitor
- `log_file` (str, optional): File to save DNS logs
- `callback` (callable, optional): Function to call for each DNS request
- `verbose` (bool): Enable verbose logging

**Returns:**
- `threading.Thread`: Thread object running the monitoring

#### `analyze_dns_logs(log_file)`

Analyze DNS logs and provide statistics.

**Parameters:**
- `log_file` (str): Path to DNS log file (JSON format)

**Returns:**
- `Dict[str, Any]`: Dictionary containing analysis results

**Raises:**
- `FileNotFoundError`: If log file not found
- `ValueError`: If invalid JSON in log file

#### `get_network_interfaces()`

Get list of available network interfaces.

**Returns:**
- `List[Dict[str, str]]`: List of interface information

### CLI Commands

The network module provides the following CLI commands:

#### `knsock scan <range> [options]`

Scan network for devices using ARP.

**Arguments:**
- `range`: Network range to scan (e.g., 192.168.1.0/24)
- `--interface`: Network interface to use (auto-detect if not specified)
- `--timeout`: Timeout in seconds for each ARP request (default: 2)
- `--verbose`: Enable verbose output

**Example:**
```bash
knsock scan 192.168.1.0/24 --verbose
```

#### `knsock mac-lookup <mac> [options]`

Lookup MAC address vendor information.

**Arguments:**
- `mac`: MAC address to lookup (e.g., 00:1A:2B:3C:4D:5E)
- `--offline`: Use offline lookup only (no API calls)
- `--api-key`: API key for macvendors.co (optional)

**Example:**
```bash
knsock mac-lookup 00:1A:2B:3C:4D:5E --offline
```

#### `knsock monitor [options]`

Monitor DNS requests on the network.

**Arguments:**
- `--duration`: Duration to monitor in seconds (default: 60)
- `--interface`: Network interface to monitor (auto-detect if not specified)
- `--log`: File to save DNS logs (JSON format)
- `--verbose`: Enable verbose output

**Example:**
```bash
knsock monitor --duration 120 --log dns_log.json --verbose
```

### Dependencies

The network module requires the following optional dependencies:

- **scapy**: For ARP scanning and DNS monitoring
  ```bash
  pip install scapy
  ```

- **psutil**: For network interface detection
  ```bash
  pip install psutil
  ```

- **requests**: For MAC vendor API lookups
  ```bash
  pip install requests
  ```

### Security and Legal Considerations

⚠️ **IMPORTANT LEGAL NOTICE:**

1. **Authorization Required**: Only use these tools on networks you own or have explicit permission to monitor.

2. **Legal Compliance**: Network monitoring may be subject to local laws and regulations. Ensure compliance with applicable privacy and surveillance laws.

3. **Ethical Use**: These tools should only be used for legitimate network administration, security testing, or educational purposes.

4. **Privilege Requirements**: Some functions require root/administrator privileges for packet sniffing.

5. **Data Privacy**: Be mindful of sensitive information that may be captured during monitoring.

### Troubleshooting

**Common Issues:**

1. **Permission Denied**: Run with `sudo` or as administrator for packet sniffing operations.

2. **Scapy Import Error**: Install scapy with `pip install scapy`.

3. **No Devices Found**: Check network range and interface selection.

4. **API Rate Limits**: Use offline mode or provide API key for MAC lookups.

5. **Interface Detection**: Manually specify interface if auto-detection fails.