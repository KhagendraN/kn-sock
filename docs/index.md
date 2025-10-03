
# kn-sock
- **[Documentation](https://kn-sock.khagendraneupane.com.np/)** 

![PyPI version](https://img.shields.io/pypi/v/kn-sock)

A simplified socket programming toolkit for Python that makes network communication easy and efficient.

## Features

- **TCP/UDP Messaging**: Supports both synchronous and asynchronous communication
- **Secure Communication**: SSL/TLS support for encrypted connections
- **JSON Socket Communication**: Easily send and receive JSON data over sockets
- **File Transfer**: Transfer files between clients and servers with progress tracking
- **Live Streaming**: Multi-video streaming with adaptive bitrate
- **Video Chat**: Real-time multi-client video chat with voice
- **WebSocket Support**: Full WebSocket server and client implementation
- **HTTP/HTTPS**: Simple HTTP client and server helpers
- **Pub/Sub & RPC**: Publish/subscribe messaging and remote procedure calls
- **Message Queuing**: Advanced queue management for reliable message delivery
- **Load Balancing**: Distribute connections across multiple servers
- **Data Compression**: Built-in compression for bandwidth optimization
- **Protocol Buffers**: Support for efficient binary serialization
- **Decorators & Utilities**: Helper decorators and utility functions
- **Docker Support**: Ready-to-use Docker containers and compose files
- **Interactive CLI**: Real-time interactive command-line interface
- **Command-Line Interface**: Simple CLI for quick socket operations
- **Connection Pooling**: Efficient connection reuse for high-performance applications
- **Network Visibility**: ARP scanning, MAC lookup, and DNS monitoring tools

## Installation

```bash
pip install kn-sock
```

## Quick Start

Here's a simple example to get you started:

```python
# Server
from kn_sock import start_tcp_server

def handle_message(data, addr, client_socket):
    print(f"Received from {addr}: {data.decode('utf-8')}")
    client_socket.sendall(b"Message received!")

start_tcp_server(8080, handle_message)
```

```python
# Client
from kn_sock import send_tcp_message

send_tcp_message("localhost", 8080, "Hello, World!")
```

### Docker Quick Start

```bash
# Run with Docker Compose
docker-compose run knsock --help

# Run tests
docker-compose run test
```

For detailed Docker usage, see the [Docker guide](https://github.com/KhagendraN/kn-sock/blob/main/docs/docker.md).

## What's Next?

- **[Getting Started](https://github.com/KhagendraN/kn-sock/blob/main/docs/getting-started.md)** - Learn the basics and set up your first project
- **[Docker Setup](https://github.com/KhagendraN/kn-sock/blob/main/docs/docker.md)** - Get started with Docker containers and deployment

### Protocol Documentation
- **[TCP Protocol](https://github.com/KhagendraN/kn-sock/blob/main/docs/protocols/tcp.md)** - Reliable connection-based communication
- **[UDP Protocol](https://github.com/KhagendraN/kn-sock/blob/main/docs/protocols/udp.md)** - Fast connectionless messaging
- **[WebSocket Protocol](https://github.com/KhagendraN/kn-sock/blob/main/docs/protocols/websocket.md)** - Real-time bidirectional communication
- **[JSON Communication](https://github.com/KhagendraN/kn-sock/blob/main/docs/protocols/json.md)** - Structured data exchange
- **[File Transfer](https://github.com/KhagendraN/kn-sock/blob/main/docs/protocols/file-transfer.md)** - Efficient file sharing
- **[Secure TCP (SSL/TLS)](https://github.com/KhagendraN/kn-sock/blob/main/docs/protocols/secure-tcp.md)** - Encrypted communication

### Advanced Features
- **[Pub/Sub Messaging](https://github.com/KhagendraN/kn-sock/blob/main/docs/advanced/pubsub.md)** - Event-driven messaging patterns
- **[Remote Procedure Calls](https://github.com/KhagendraN/kn-sock/blob/main/docs/advanced/rpc.md)** - Call remote functions seamlessly
- **[Live Streaming](https://github.com/KhagendraN/kn-sock/blob/main/docs/advanced/live-streaming.md)** - Multi-video streaming with adaptive bitrate
- **[Video Chat](https://github.com/KhagendraN/kn-sock/blob/main/docs/advanced/video-chat.md)** - Real-time video conferencing
- **[HTTP/HTTPS](https://github.com/KhagendraN/kn-sock/blob/main/docs/advanced/http.md)** - Web server and client functionality

### Reference & Examples
- **[API Reference](https://github.com/KhagendraN/kn-sock/blob/main/docs/api-reference.md)** - Complete function and class documentation
- **[CLI Guide](https://github.com/KhagendraN/kn-sock/blob/main/docs/cli.md)** - Command-line interface usage
- **[Examples](https://github.com/KhagendraN/kn-sock/blob/main/docs/examples.md)** - Real-world usage examples
- **[Troubleshooting](https://github.com/KhagendraN/kn-sock/blob/main/docs/troubleshooting.md)** - Common issues and solutions

## Network Visibility Tools

⚠️ **ETHICAL WARNING**: These tools are intended for use in authorized networks such as schools, labs, or controlled IT environments. Monitoring user traffic may be illegal without explicit consent. Use responsibly and ethically.

### Network Monitoring
- **[ARP Scanning](https://github.com/KhagendraN/kn-sock/blob/main/docs/network/arp.md)** - Discover active devices on your network
- **[MAC Address Lookup](https://github.com/KhagendraN/kn-sock/blob/main/docs/network/maclookup.md)** - Identify device vendors by MAC address
- **[DNS Monitoring](https://github.com/KhagendraN/kn-sock/blob/main/docs/network/monitor.md)** - Monitor and analyze DNS requests
