# UDP Utilities

`kn-sock` provides a set of UDP tools for sending and receiving datagrams over IPv4 or IPv6, with support for both synchronous and asynchronous workflows. It also includes utilities for multicast communication.

Use these tools to build, test, and automate UDP-based communication in your scripts or applications.

## Function Index

| Function/Class                    | Description |
|----------------------------------|-------------|
| [start_udp_server](reference.md#kn_sock.udp.start_udp_server) | Starts a basic synchronous UDP server with graceful shutdown support. |
| [send_udp_message](reference.md#kn_sock.udp.send_udp_message) | Sends a UTF-8 message to a UDP server. |
| [start_udp_server_async](reference.md#kn_sock.udp.start_udp_server_async) | Starts an asynchronous UDP server using `asyncio`. |
| [send_udp_message_async](reference.md#kn_sock.udp.send_udp_message_async) | Sends a message to a UDP server asynchronously. |
| [start_udp_multicast_server](reference.md#kn_sock.udp.start_udp_multicast_server) | Starts a server that listens for multicast messages on a group and port. |
| [send_udp_multicast](reference.md#kn_sock.udp.send_udp_multicast) | Sends a multicast message to a specific group and port. |

## When to Use UDP

- Low-latency or broadcast-style communication
- Fire-and-forget messages (no connection state)
- Multicast discovery or distributed coordination
- Non-blocking async I/O with high throughput

For reliable or ordered delivery, consider using [TCP Utilities](../tcp/index.md).

## Related Topics

- [Using the CLI](cli.md)
- [Using the Python API](python-api.md)
- [API Reference](reference.md)
- [Testing & Troubleshooting](testing.md)