# kn-sock API Reference

The kn-sock library offers a modern, Pythonic toolkit for socket programming, including TCP/UDP messaging, file transfer, live streaming, WebSockets, JSON sockets, pub/sub, and more.
  
All features are available as both Python API functions and convenient CLI commands for rapid testing and automation.

**Quick Links:**
- [TCP Utilities](tcp.md)
- [UDP Utilities](udp.md)
- [HTTP/HTTPS Utilities](http.md)
- [WebSocket Utilities](websocket.md)
- [JSON Messaging](json.md)
- [File Transfer](file_transfer.md)
- [Live Streaming](live_stream.md)
- [Pub/Sub Messaging](pubsub.md)
- [RPC Utilities](rpc.md)
- [Queues & Threading](queue.md)
- [Configuration Utilities](config.md)
- [Troubleshooting](troubleshooting.md)

## Key Features

| Feature              | Python API         | CLI Command(s)          | Purpose / Use Case                                  |
|----------------------|-------------------|-------------------------|-----------------------------------------------------|
| TCP/UDP Messaging    | Yes               | Yes                     | Network echo/test servers, quick data exchange      |
| File Transfer        | Yes               | Yes                     | Move files between machines via TCP                 |
| WebSocket            | Yes               | Yes                     | Modern browser/client real-time comms               |
| HTTP/HTTPS           | Yes               | Yes                     | Lightweight HTTP servers/clients                    |
| Live Streaming       | Yes               | Yes                     | Video/audio streaming across clients (FFmpeg/OpenCV)|
| Pub/Sub              | Yes               | Yes                     | Message broadcasting and topic subscriptions        |
| RPC                  | Yes               | Yes                     | Remote procedure call/test microservices            |
| JSON Sockets         | Yes               | Yes                     | Send/receive structured data easily                 |
| Interactive CLI      | —                 | Yes                     | Run all CLI features with guided prompts            |

## How to Use

You can use kn-sock in two main ways:

1. **From the command line:**  
   Quickly spin up servers, clients, or file transfers with a single command.  
   See each protocol’s page for sample commands.

2. **As a Python library:**  
   Import and use the utilities in your own scripts or apps.
   ```python
   from kn_sock import start_tcp_server, send_tcp_message
   # ... your code ...
