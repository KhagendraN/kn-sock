# HTTP/HTTPS

kn-sock provides simple HTTP and HTTPS client helpers and a basic HTTP server for serving static files and handling API routes.

## HTTP Client

### Basic HTTP GET

```python
from kn_sock import http_get

# Simple GET request
response = http_get("example.com", 80, "/")
print(response)

# GET with custom headers
headers = {
    "User-Agent": "kn-sock/1.0",
    "Accept": "application/json"
}
response = http_get("api.example.com", 80, "/users", headers=headers)
print(response)
```

### HTTP POST

```python
from kn_sock import http_post

# POST with form data
data = "name=John&email=john@example.com"
response = http_post("api.example.com", 80, "/users", data=data)

# POST with JSON data
import json
json_data = json.dumps({"name": "John", "email": "john@example.com"})
headers = {"Content-Type": "application/json"}
response = http_post("api.example.com", 80, "/users", data=json_data, headers=headers)
```

## HTTPS Client

### HTTPS GET

```python
from kn_sock import https_get

# Simple HTTPS GET
response = https_get("example.com", 443, "/")
print(response)

# HTTPS GET with certificate verification
response = https_get("api.example.com", 443, "/secure", cafile="ca.crt")
```

### HTTPS POST

```python
from kn_sock import https_post

# HTTPS POST with JSON
import json
data = json.dumps({"action": "login", "username": "user", "password": "pass"})
headers = {"Content-Type": "application/json"}

response = https_post("api.example.com", 443, "/auth", data=data, headers=headers)
print(response)
```

## HTTP Server

### Basic HTTP Server

```python
from kn_sock import start_http_server

# Start server serving static files
start_http_server("127.0.0.1", 8080, static_dir="/path/to/static/files")
```

### HTTP Server with Custom Routes

```python
from kn_sock import start_http_server
import json

def hello_handler(request, client_socket):
    """Handle /hello route"""
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nHello"
    client_socket.sendall(response.encode())

def api_handler(request, client_socket):
    """Handle /api route"""
    data = {"message": "Hello from API", "status": "success"}
    response_json = json.dumps(data)
    
    response = f"""HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: {len(response_json)}

{response_json}"""
    client_socket.sendall(response.encode())

def echo_handler(request, client_socket):
    """Handle POST /echo route"""
    # Extract body from request
    body = request['raw'].decode('utf-8').split('\r\n\r\n', 1)[-1]
    
    response = f"""HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: {len(body)}

{body}"""
    client_socket.sendall(response.encode())

# Define routes
routes = {
    ("GET", "/hello"): hello_handler,
    ("GET", "/api"): api_handler,
    ("POST", "/echo"): echo_handler,
}

# Start server with routes
start_http_server("127.0.0.1", 8080, static_dir="static", routes=routes)
```
## Limitations

### Current Limitations

- No support for redirects
- No support for chunked encoding
- No support for cookies
- No support for HTTP/2
- Limited header parsing
- No support for streaming responses

## Related Topics

- **[TCP Protocol](../protocols/tcp.md)** - For underlying transport
- **[Secure TCP](../protocols/secure-tcp.md)** - For HTTPS functionality
- **[API Reference](../api-reference.md)** - For complete function documentation 