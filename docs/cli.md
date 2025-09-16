# Command-Line Interface

kn-sock provides a comprehensive command-line interface for quick socket operations and testing.

## Overview

The `kn-sock` CLI allows you to:
- Start servers for various protocols
- Send messages and files
- Connect to live streams and video chat
- Use interactive mode for real-time communication
- Test network connectivity

## Basic Commands

### TCP Commands

#### Start TCP Server

```bash
kn-sock run-tcp-server <port>
```

**Options:**
- `--host <host>`: Host to bind (default: 0.0.0.0)

**Example:**
```bash
kn-sock run-tcp-server 8080
kn-sock run-tcp-server 8080 --host 127.0.0.1
```

#### Send TCP Message

```bash
kn-sock send-tcp <host> <port> <message>
```

**Example:**
```bash
kn-sock send-tcp localhost 8080 "Hello, World!"
kn-sock send-tcp 192.168.1.10 8080 "Test message"
```

### UDP Commands

#### Start UDP Server

```bash
kn-sock run-udp-server <port>
```

**Options:**
- `--host <host>`: Host to bind (default: 0.0.0.0)

**Example:**
```bash
kn-sock run-udp-server 8080
```

#### Send UDP Message

```bash
kn-sock send-udp <host> <port> <message>
```

**Example:**
```bash
kn-sock send-udp localhost 8080 "Hello, UDP!"
```

#### Send UDP Multicast

```bash
kn-sock send-udp-multicast <group> <port> <message>
```

**Options:**
- `--ttl <ttl>`: Time-to-live for multicast packets (default: 1)

**Example:**
```bash
kn-sock send-udp-multicast 224.0.0.1 8080 "Multicast message"
```

### Secure TCP (SSL/TLS) Commands

#### Start Secure TCP Server

```bash
kn-sock run-ssl-tcp-server <port> <certfile> <keyfile>
```

**Options:**
- `--host <host>`: Host to bind (default: 0.0.0.0)
- `--cafile <cafile>`: CA certificate for client verification
- `--require-client-cert`: Require client certificates (mutual TLS)

**Example:**
```bash
kn-sock run-ssl-tcp-server 8443 server.crt server.key
kn-sock run-ssl-tcp-server 8443 server.crt server.key --cafile ca.crt --require-client-cert
```

#### Send Secure TCP Message

```bash
kn-sock send-ssl-tcp <host> <port> <message>
```

**Options:**
- `--cafile <cafile>`: CA certificate for server verification
- `--certfile <certfile>`: Client certificate
- `--keyfile <keyfile>`: Client private key
- `--no-verify`: Disable server certificate verification

**Example:**
```bash
kn-sock send-ssl-tcp localhost 8443 "Hello Secure"
kn-sock send-ssl-tcp localhost 8443 "Hello Secure" --cafile ca.crt --certfile client.crt --keyfile client.key
```

### File Transfer Commands

#### Start File Server

```bash
kn-sock run-file-server <port> <save_directory>
```

**Options:**
- `--host <host>`: Host to bind (default: 0.0.0.0)

**Example:**
```bash
kn-sock run-file-server 8080 /path/to/save/directory
```

#### Send File

```bash
kn-sock send-file <host> <port> <filepath>
```

**Options:**
- `--show-progress`: Show progress bar (default: true)
- `--no-progress`: Hide progress bar

**Example:**
```bash
kn-sock send-file localhost 8080 /path/to/file.txt
kn-sock send-file localhost 8080 large_file.zip --show-progress
```

### JSON Commands

#### Send JSON Data

```bash
kn-sock send-json <host> <port> <json_data>
```

**Example:**
```bash
kn-sock send-json localhost 8080 '{"message": "Hello", "type": "greeting"}'
kn-sock send-json localhost 8080 '{"user_id": 123, "action": "login"}'
```

### WebSocket Commands

#### Start WebSocket Server

```bash
kn-sock run-websocket-server <host> <port>
```

**Example:**
```bash
kn-sock run-websocket-server 127.0.0.1 8765
```

#### Connect to WebSocket

```bash
kn-sock connect-websocket <host> <port>
```

**Options:**
- `--resource <path>`: WebSocket resource path (default: /)
- `--headers <json>`: Additional headers as JSON

**Example:**
```bash
kn-sock connect-websocket localhost 8765
kn-sock connect-websocket localhost 8765 --resource /chat --headers '{"Authorization": "Bearer token"}'
```

### HTTP Commands

#### Start HTTP Server

```bash
kn-sock run-http-server <host> <port>
```

**Options:**
- `--static-dir <directory>`: Directory to serve static files
- `--routes <json>`: Custom routes as JSON

**Example:**
```bash
kn-sock run-http-server 127.0.0.1 8080
kn-sock run-http-server 127.0.0.1 8080 --static-dir /path/to/static
```

#### HTTP GET Request

```bash
kn-sock http-get <host> <port> <path>
```

**Options:**
- `--headers <json>`: HTTP headers as JSON

**Example:**
```bash
kn-sock http-get example.com 80 /
kn-sock http-get api.example.com 443 /users --headers '{"Authorization": "Bearer token"}'
```

#### HTTP POST Request

```bash
kn-sock http-post <host> <port> <path> <data>
```

**Options:**
- `--headers <json>`: HTTP headers as JSON

**Example:**
```bash
kn-sock http-post api.example.com 80 /users '{"name": "John", "email": "john@example.com"}'
```

### Pub/Sub Commands

#### Start Pub/Sub Server

```bash
kn-sock run-pubsub-server <port>
```

**Options:**
- `--host <host>`: Host to bind (default: 0.0.0.0)

**Example:**
```bash
kn-sock run-pubsub-server 9000
```

#### Pub/Sub Client Commands

```bash
# Subscribe to a topic
kn-sock pubsub-subscribe <host> <port> <topic>

# Publish a message
kn-sock pubsub-publish <host> <port> <topic> <message>

# Receive messages
kn-sock pubsub-receive <host> <port>
```

**Example:**
```bash
kn-sock pubsub-subscribe localhost 9000 news
kn-sock pubsub-publish localhost 9000 news "Breaking news!"
kn-sock pubsub-receive localhost 9000
```

### RPC Commands

#### Start RPC Server

```bash
kn-sock run-rpc-server <port>
```

**Options:**
- `--host <host>`: Host to bind (default: 0.0.0.0)
- `--functions <json>`: Functions to register as JSON

**Example:**
```bash
kn-sock run-rpc-server 9001
kn-sock run-rpc-server 9001 --functions '{"add": "lambda x, y: x + y", "echo": "lambda msg: msg"}'
```

#### RPC Client Commands

```bash
# Call a remote function
kn-sock rpc-call <host> <port> <function> <args...>
```

**Example:**
```bash
kn-sock rpc-call localhost 9001 add 2 3
kn-sock rpc-call localhost 9001 echo "Hello RPC"
```

### Live Streaming Commands

#### Start Live Stream Server

```bash
kn-sock run-live-server <port> <video_files...>
```

**Options:**
- `--host <host>`: Host to bind (default: 0.0.0.0)
- `--audio-port <port>`: Audio port (default: port + 1)

**Example:**
```bash
kn-sock run-live-server 9000 video1.mp4 video2.mp4 video3.mp4
kn-sock run-live-server 9000 movie.mp4 --host 0.0.0.0 --audio-port 9001
```

#### Connect to Live Stream

```bash
kn-sock connect-live-server <host> <port>
```

**Options:**
- `--audio-port <port>`: Audio port (default: port + 1)

**Example:**
```bash
kn-sock connect-live-server 192.168.1.10 9000
kn-sock connect-live-server 192.168.1.10 9000 --audio-port 9001
```

### Video Chat Commands

#### Start Video Chat Server

```bash
kn-sock run-video-chat-server
```

**Options:**
- `--host <host>`: Host to bind (default: 0.0.0.0)
- `--video-port <port>`: Video port (default: 9000)
- `--audio-port <port>`: Audio port (default: 9001)
- `--text-port <port>`: Text port (default: 9002)

**Example:**
```bash
kn-sock run-video-chat-server
kn-sock run-video-chat-server --host 0.0.0.0 --video-port 9000 --audio-port 9001 --text-port 9002
```

#### Connect to Video Chat

```bash
kn-sock connect-video-chat <server_ip> <room> <nickname>
```

**Options:**
- `--video-port <port>`: Video port (default: 9000)
- `--audio-port <port>`: Audio port (default: 9001)
- `--text-port <port>`: Text port (default: 9002)
- `--no-audio`: Disable audio functionality

**Example:**
```bash
kn-sock connect-video-chat 127.0.0.1 myroom alice
kn-sock connect-video-chat 192.168.1.10 conference john --video-port 9000 --audio-port 9001 --text-port 9002
```

## Interactive Mode

### Start Interactive CLI

```bash
kn-sock interactive
```

### Interactive Commands

Once in interactive mode, you can use these commands:

#### Connection Management

```bash
# Connect to a server
connect <name> <host> <port>

# List all connections
list

# Select default connection
select <name>

# Disconnect a connection
disconnect <name>
```

#### Communication

```bash
# Send a message
send <message>

# Receive a message
receive

# Toggle background receive mode
bg_receive

# Show message history
history
```

#### Utility

```bash
# Show help
help

# Exit the CLI
quit
exit
```

### Interactive Session Example

```bash
$ kn-sock interactive
kn-sock> connect server1 localhost 8080
Connected to localhost:8080 as 'server1'
kn-sock> send Hello, server!
Message sent
kn-sock> receive
Received: Message received!
kn-sock> bg_receive
Background receive mode enabled
kn-sock> send Another message
Message sent
Received: Message received!
kn-sock> history
Last 10 messages:
1. [SENT] Hello, server!
2. [RECV] Message received!
3. [SENT] Another message
4. [RECV] Message received!
kn-sock> disconnect server1
Disconnected from server1
kn-sock> quit
```

## Global Options

All commands support these global options:

- `--help`, `-h`: Show help message
- `--version`, `-v`: Show version information
- `--verbose`: Enable verbose output
- `--quiet`: Suppress output (except errors)

## Examples

### Complete Workflow Examples

#### TCP Echo Server and Client

```bash
# Terminal 1: Start server
kn-sock run-tcp-server 8080

# Terminal 2: Send message
kn-sock send-tcp localhost 8080 "Hello, World!"
```

#### File Transfer

```bash
# Terminal 1: Start file server
kn-sock run-file-server 8080 /tmp/received

# Terminal 2: Send file
kn-sock send-file localhost 8080 /path/to/document.pdf
```

#### Secure Communication

```bash
# Terminal 1: Start secure server
kn-sock run-ssl-tcp-server 8443 server.crt server.key

# Terminal 2: Send secure message
kn-sock send-ssl-tcp localhost 8443 "Secret message"
```

#### Live Streaming

```bash
# Terminal 1: Start live stream server
kn-sock run-live-server 9000 movie.mp4

# Terminal 2: Connect as client
kn-sock connect-live-server 192.168.1.10 9000
```

#### Video Chat

```bash
# Terminal 1: Start video chat server
kn-sock run-video-chat-server

# Terminal 2: Connect as client
kn-sock connect-video-chat 127.0.0.1 meeting alice

# Terminal 3: Connect another client
kn-sock connect-video-chat 127.0.0.1 meeting bob
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Use a different port
   kn-sock run-tcp-server 8081
   ```

2. **Permission denied**
   ```bash
   # Use a higher port number
   kn-sock run-tcp-server 8080
   ```

3. **Connection refused**
   ```bash
   # Make sure server is running first
   kn-sock run-tcp-server 8080 &
   kn-sock send-tcp localhost 8080 "test"
   ```

4. **SSL certificate issues**
   ```bash
   # For testing, disable verification
   kn-sock send-ssl-tcp localhost 8443 "test" --no-verify
   ```

### Debug Mode

Enable verbose output for debugging:

```bash
kn-sock --verbose run-tcp-server 8080
kn-sock --verbose send-tcp localhost 8080 "test"
```

## Related Topics

- **[Getting Started](getting-started.md)** - For basic usage examples
- **[Interactive CLI](advanced/interactive-cli.md)** - For detailed interactive mode documentation
- **[API Reference](api-reference.md)** - For programmatic usage 