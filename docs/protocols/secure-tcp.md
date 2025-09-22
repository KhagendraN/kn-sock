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
    8443,
    handle_secure,
    certfile="server.crt",
    keyfile="server.key"
)
```

### Synchronous Secure TCP Client

```python
from kn_sock import send_ssl_tcp_message

send_ssl_tcp_message(
    "localhost", 8443, "Hello Secure"
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

## Security Best Practices

### Certificate Validation

```python
from kn_sock import send_ssl_tcp_message

# Always verify server certificates in production
send_ssl_tcp_message(
    "example.com", 443, "Hello",
    cafile="trusted_ca.crt",
    verify=True
)

# For testing only - disable verification
send_ssl_tcp_message(
    "localhost", 8443, "Hello",
    verify=False  # Only for development/testing
)
```

### Strong Cipher Suites

```python
import ssl
from kn_sock import start_ssl_tcp_server

def create_secure_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    # Set strong cipher suites
    context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256')
    
    # Set minimum TLS version
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    
    return context

start_ssl_tcp_server(
    8443,
    handle_secure,
    ssl_context=create_secure_context()
)
```

### Certificate Revocation

```python
import ssl
from kn_sock import start_ssl_tcp_server

def create_context_with_crl():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    context.load_verify_locations(cafile="ca.crt", capath=None, cadata=None)
    
    # Load certificate revocation list
    context.load_verify_locations(cafile="ca.crt")
    context.verify_flags = ssl.VERIFY_CRL_CHECK_LEAF
    
    return context
```

## Error Handling

### SSL/TLS Errors

```python
from kn_sock.errors import EasySocketError
import ssl

try:
    send_ssl_tcp_message("localhost", 8443, "Hello")
except ssl.SSLError as e:
    print(f"SSL error: {e}")
except EasySocketError as e:
    print(f"Socket error: {e}")
```

### Certificate Validation Errors

```python
import ssl

try:
    send_ssl_tcp_message(
        "localhost", 8443, "Hello",
        cafile="ca.crt",
        verify=True
    )
except ssl.SSLCertVerificationError as e:
    print(f"Certificate verification failed: {e}")
except ssl.SSLError as e:
    print(f"SSL error: {e}")
```

## Connection Pooling with SSL

### Secure Connection Pool

```python
from kn_sock import TCPConnectionPool

pool = TCPConnectionPool(
    'localhost', 8443, max_size=5, idle_timeout=30,
    ssl=True, 
    cafile="ca.crt", 
    certfile="client.crt", 
    keyfile="client.key", 
    verify=True
)

with pool.connection() as conn:
    conn.sendall(b"Hello Secure")
    data = conn.recv(1024)
    print(data)

pool.closeall()
```

## Use Cases

### Secure API Server

```python
from kn_sock import start_ssl_tcp_server
import json

def handle_api_request(data, addr, client_socket):
    try:
        request = json.loads(data.decode())
        endpoint = request.get('endpoint')
        
        if endpoint == 'get_data':
            response = {"status": "success", "data": "sensitive_data"}
        else:
            response = {"status": "error", "message": "Unknown endpoint"}
        
        client_socket.sendall(json.dumps(response).encode())
    except json.JSONDecodeError:
        error_response = {"status": "error", "message": "Invalid JSON"}
        client_socket.sendall(json.dumps(error_response).encode())

start_ssl_tcp_server(
    8443,
    handle_api_request,
    certfile="api_server.crt",
    keyfile="api_server.key",
    cafile="ca.crt",
    require_client_cert=True
)
```

### Secure File Transfer

```python
from kn_sock import start_ssl_tcp_server, send_ssl_tcp_message

def handle_secure_file_transfer(data, addr, client_socket):
    # Handle secure file transfer
    filename = data.decode().strip()
    
    try:
        with open(filename, 'rb') as f:
            file_data = f.read()
        
        # Send file size first
        size_msg = f"SIZE:{len(file_data)}".encode()
        client_socket.sendall(size_msg)
        
        # Send file data
        client_socket.sendall(file_data)
        
    except FileNotFoundError:
        error_msg = "ERROR:File not found".encode()
        client_socket.sendall(error_msg)

start_ssl_tcp_server(
    8443,
    handle_secure_file_transfer,
    certfile="file_server.crt",
    keyfile="file_server.key"
)
```

### Database Connection Proxy

```python
from kn_sock import start_ssl_tcp_server
import psycopg2

def handle_db_query(data, addr, client_socket):
    try:
        query = data.decode()
        
        # Connect to database
        conn = psycopg2.connect(
            host="localhost",
            database="myapp",
            user="dbuser",
            password="dbpass"
        )
        
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        response = {"status": "success", "data": result}
        client_socket.sendall(json.dumps(response).encode())
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        error_response = {"status": "error", "message": str(e)}
        client_socket.sendall(json.dumps(error_response).encode())

start_ssl_tcp_server(
    8443,
    handle_db_query,
    certfile="db_proxy.crt",
    keyfile="db_proxy.key",
    cafile="ca.crt",
    require_client_cert=True
)
```

## CLI Usage

```bash
# Start a secure server
kn-sock run-ssl-tcp-server 8443 server.crt server.key

# Start with client certificate verification
kn-sock run-ssl-tcp-server 8443 server.crt server.key --cafile ca.crt --require-client-cert

# Send a secure message
kn-sock send-ssl-tcp localhost 8443 "Hello Secure"

# Send with client certificate
kn-sock send-ssl-tcp localhost 8443 "Hello Secure" --cafile ca.crt --certfile client.crt --keyfile client.key
```

## Security Checklist

- [ ] Use strong private keys (2048+ bits)
- [ ] Validate server certificates in production
- [ ] Use CA-signed certificates for production
- [ ] Implement certificate revocation checking
- [ ] Use strong cipher suites
- [ ] Set minimum TLS version to 1.2 or higher
- [ ] Regularly rotate certificates
- [ ] Monitor for certificate expiration
- [ ] Implement proper error handling
- [ ] Use mutual TLS for sensitive applications

## Troubleshooting

### Common SSL Issues

1. **Certificate verification failed**
   - Ensure CA certificate is correct
   - Check certificate expiration dates
   - Verify certificate chain

2. **Private key mismatch**
   - Ensure private key matches certificate
   - Check file permissions

3. **Cipher suite mismatch**
   - Update to supported cipher suites
   - Check TLS version compatibility

4. **Hostname verification failed**
   - Use correct hostname in certificate
   - Or disable hostname verification for testing

## Related Topics

- **[TCP Protocol](tcp.md)** - For basic TCP communication
- **[Connection Pooling](tcp.md#tcp-connection-pooling)** - For efficient secure connections
- **[API Reference](../api-reference.md)** - Complete function documentation 