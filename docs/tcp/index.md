# TCP Utilities

`kn-sock` provides both CLI commands and a Python API for building, testing, and automating TCP server–client communication. You can use it for basic network testing, multi-client echo servers, encrypted TLS communication, and connection pooling.

Choose the interface that suits your workflow:

- Use the **CLI** to run quick tests or scripts in Docker.
- Use the **Python API** to integrate TCP utilities into your applications.

## Function Index

| Function/Class | Description |
|--|--|
| [start_tcp_server](reference.md#kn_sock.tcp.start_tcp_server) | Basic synchronous TCP server for single-connection, blocking I/O. |
| [start_threaded_tcp_server](reference.md#kn_sock.tcp.start_threaded_tcp_server) | Multithreaded TCP server that spawns a thread per client. |
| [send_tcp_message](reference.md#kn_sock.tcp.send_tcp_message) | Sync TCP client that sends a UTF-8 message and logs the response. |
| [send_tcp_bytes](reference.md#kn_sock.tcp.send_tcp_bytes) | Sync TCP client for sending raw bytes. |
| [start_async_tcp_server](reference.md#kn_sock.tcp.start_async_tcp_server) | Async TCP server using `asyncio`. |
| [send_tcp_message_async](reference.md#kn_sock.tcp.send_tcp_message_async) | Async TCP client for sending messages without blocking. |
| [TCPConnectionPool](reference.md#kn_sock.tcp.TCPConnectionPool) | Thread-safe pool for managing reusable TCP (and SSL) connections. |
| [start_ssl_tcp_server](reference.md#kn_sock.tcp.start_ssl_tcp_server) | Synchronous TCP server with TLS/mTLS support. |
| [send_ssl_tcp_message](reference.md#kn_sock.tcp.send_ssl_tcp_message) | TLS-enabled sync client for secure message exchange. |
| [start_async_ssl_tcp_server](reference.md#kn_sock.tcp.start_async_ssl_tcp_server) | Async TLS server using `asyncio`. |
| [send_ssl_tcp_message_async](reference.md#kn_sock.tcp.send_ssl_tcp_message_async) | Async TLS client using non-blocking secure sockets. |

## Quick Links

- [Using the CLI](cli.md)
- [Using the Python API](python-api.md)
- [API Reference](reference.md)
- [Testing & Troubleshooting](testing.md)