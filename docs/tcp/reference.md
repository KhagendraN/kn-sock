# API Reference

This page documents all public classes and functions available in the `kn_sock.tcp` module. You can use these directly in your Python applications or scripts.

## TCP Server APIs

### Synchronous Servers

::: kn_sock.tcp.start_tcp_server
    options:
      show_root_heading: true
      show_source: false

::: kn_sock.tcp.start_threaded_tcp_server
    options:
      show_root_heading: true
      show_source: false

---

### Asynchronous Servers

::: kn_sock.tcp.start_async_tcp_server
    options:
      show_root_heading: true
      show_source: false

---

## TCP Client APIs

### Synchronous Clients

::: kn_sock.tcp.send_tcp_message
    options:
      show_root_heading: true
      show_source: false

::: kn_sock.tcp.send_tcp_bytes
    options:
      show_root_heading: true
      show_source: false

---

### Asynchronous Clients

::: kn_sock.tcp.send_tcp_message_async
    options:
      show_root_heading: true
      show_source: false

---

## Connection Pooling

::: kn_sock.tcp.TCPConnectionPool
    options:
      show_root_heading: true
      show_source: false

---

## SSL/TLS Servers

### Synchronous

::: kn_sock.tcp.start_ssl_tcp_server
    options:
      show_root_heading: true
      show_source: false

### Asynchronous

::: kn_sock.tcp.start_async_ssl_tcp_server
    options:
      show_root_heading: true
      show_source: false

---

## SSL/TLS Clients

### Synchronous

::: kn_sock.tcp.send_ssl_tcp_message
    options:
      show_root_heading: true
      show_source: false

### Asynchronous

::: kn_sock.tcp.send_ssl_tcp_message_async
    options:
      show_root_heading: true
      show_source: false