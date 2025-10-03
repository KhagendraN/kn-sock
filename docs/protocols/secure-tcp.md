# Secure TCP (SSL/TLS)

kn-sock provides comprehensive SSL/TLS support for secure, encrypted communication over TCP connections.

## Overview

Secure TCP features in kn-sock:
- Full SSL/TLS encryption support
- Both synchronous and asynchronous operations
- Client and server certificate validation
- Mutual TLS (mTLS) support
- Configurable security parameters
- Integration with connection pooling

## Basic SSL/TLS Setup

### Synchronous Secure TCP Server

```python
from kn_sock import start_ssl_tcp_server

def handle_secure(data, addr, client_socket):
    print(f"Received from {addr}: {data.decode()}")
    client_socket.sendall(b"Secure response")

start_ssl_tcp_server(
    port=8443,
    handler_func=handle_secure,
    certfile="server.crt",
    keyfile="server.key",
    cafile="ca.crt",  # Optional, for client cert verification
    require_client_cert=True,  # Optional, for mutual TLS
    host="0.0.0.0"  # Optional, defaults to "0.0.0.0"
)
```

### Synchronous Secure TCP Client

```python
from kn_sock import send_ssl_tcp_message

send_ssl_tcp_message(
    host="localhost",
    port=8443,
    message="Hello Secure",
    cafile="ca.crt",  # Optional, for server verification
    certfile="client.crt",  # Optional, for mutual TLS
    keyfile="client.key",   # Optional, for mutual TLS
    verify=True  # Optional, defaults to True
)
```

## Asynchronous SSL/TLS

### Async Secure TCP Server

```python
import asyncio
from kn_sock import start_async_ssl_tcp_server

async def handle_secure(data, addr, writer):
    print(f"Received from {addr}: {data.decode()}")
    writer.write(b"Secure response")
    await writer.drain()

asyncio.run(start_async_ssl_tcp_server(
    8443,
    handle_secure,
    certfile="server.crt",
    keyfile="server.key"
))
```

### Async Secure TCP Client

```python
import asyncio
from kn_sock import send_ssl_tcp_message_async

asyncio.run(send_ssl_tcp_message_async(
    "localhost", 8443, "Hello Secure"
))
```

## Certificate Management

### Generating Self-Signed Certificates

For testing and development:

```bash
# Generate private key
openssl genrsa -out server.key 2048

# Generate certificate signing request
openssl req -new -key server.key -out server.csr

# Generate self-signed certificate
openssl x509 -req -in server.csr -signkey server.key -out server.crt -days 365
```

### Generating CA-Signed Certificates

For production use:

```bash
# Generate CA private key
openssl genrsa -out ca.key 2048

# Generate CA certificate
openssl req -new -x509 -key ca.key -out ca.crt -days 3650

# Generate server private key
openssl genrsa -out server.key 2048

# Generate server certificate signing request
openssl req -new -key server.key -out server.csr

# Sign server certificate with CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -out server.crt -days 365
```

### Client Certificates (mTLS)

For mutual TLS authentication:

```bash
# Generate client private key
openssl genrsa -out client.key 2048

# Generate client certificate signing request
openssl req -new -key client.key -out client.csr

# Sign client certificate with CA
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -out client.crt -days 365
```

## Advanced SSL/TLS Configuration

### Server with CA Verification

```python
from kn_sock import start_ssl_tcp_server

def handle_secure(data, addr, client_socket):
    print(f"Received from {addr}: {data.decode()}")
    client_socket.sendall(b"Secure response")

start_ssl_tcp_server(
    8443,
    handle_secure,
    certfile="server.crt",
    keyfile="server.key",
    cafile="ca.crt",  # CA certificate for client verification
    require_client_cert=True  # Require client certificates
)
```

### Client with Certificate Authentication

```python
from kn_sock import send_ssl_tcp_message

send_ssl_tcp_message(
    "localhost", 8443, "Hello Secure",
    cafile="ca.crt",  # CA certificate for server verification
    certfile="client.crt",  # Client certificate
    keyfile="client.key",  # Client private key
    verify=True  # Verify server certificate
)
```

### Custom SSL Context

```python
import ssl
from kn_sock import start_ssl_tcp_server

def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    context.load_verify_locations(cafile="ca.crt")
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    return context

def handle_secure(data, addr, client_socket):
    print(f"Received from {addr}: {data.decode()}")
    client_socket.sendall(b"Secure response")

start_ssl_tcp_server(
    8443,
    handle_secure,
    ssl_context=create_ssl_context()
)
```
## Related Topics

- **[TCP Protocol](tcp.md)** - For reliable JSON communication
- **[UDP Protocol](udp.md)** - For fast JSON messaging
- **[File Transfer](file-transfer.md)** - For large data transfer
- **[API Reference](../api-reference.md)** - Complete function documentation 