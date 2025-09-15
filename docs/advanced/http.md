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

## Use Cases

### Simple API Client

```python
from kn_sock import http_get, http_post
import json

class APIClient:
    def __init__(self, host, port=80):
        self.host = host
        self.port = port
        self.headers = {"Content-Type": "application/json"}
    
    def get_users(self):
        """Get all users"""
        response = http_get(self.host, self.port, "/api/users", headers=self.headers)
        return json.loads(response)
    
    def create_user(self, name, email):
        """Create a new user"""
        data = json.dumps({"name": name, "email": email})
        response = http_post(self.host, self.port, "/api/users", data=data, headers=self.headers)
        return json.loads(response)
    
    def update_user(self, user_id, **kwargs):
        """Update a user"""
        data = json.dumps(kwargs)
        response = http_post(self.host, self.port, f"/api/users/{user_id}", data=data, headers=self.headers)
        return json.loads(response)

# Usage
client = APIClient("api.example.com")
users = client.get_users()
new_user = client.create_user("Alice", "alice@example.com")
```

### File Upload Server

```python
from kn_sock import start_http_server
import os

def upload_handler(request, client_socket):
    """Handle file uploads"""
    try:
        # Parse multipart form data (simplified)
        body = request['raw'].decode('utf-8').split('\r\n\r\n', 1)[-1]
        
        # Extract filename and content (simplified parsing)
        if 'filename=' in body:
            filename_start = body.find('filename="') + 10
            filename_end = body.find('"', filename_start)
            filename = body[filename_start:filename_end]
            
            # Extract file content
            content_start = body.find('\r\n\r\n', body.find('Content-Type:')) + 4
            content = body[content_start:].split('\r\n--')[0]
            
            # Save file
            with open(f"uploads/{filename}", "w") as f:
                f.write(content)
            
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 20\r\n\r\nFile uploaded successfully"
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\nContent-Length: 15\r\n\r\nNo file provided"
        
        client_socket.sendall(response.encode())
        
    except Exception as e:
        error_response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\nContent-Length: {len(str(e))}\r\n\r\n{str(e)}"
        client_socket.sendall(error_response.encode())

# Create uploads directory
os.makedirs("uploads", exist_ok=True)

# Start server
routes = {("POST", "/upload"): upload_handler}
start_http_server("127.0.0.1", 8080, routes=routes)
```

### Webhook Receiver

```python
from kn_sock import start_http_server
import json
import hmac
import hashlib

class WebhookReceiver:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def verify_signature(self, payload, signature):
        """Verify webhook signature"""
        expected_signature = hmac.new(
            self.secret_key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    def handle_webhook(self, request, client_socket):
        """Handle incoming webhook"""
        try:
            # Extract headers and body
            headers = {}
            body = ""
            
            request_text = request['raw'].decode('utf-8')
            parts = request_text.split('\r\n\r\n', 1)
            
            if len(parts) > 1:
                header_text, body = parts
                
                # Parse headers
                for line in header_text.split('\r\n')[1:]:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        headers[key.strip()] = value.strip()
            
            # Verify signature
            signature = headers.get('X-Hub-Signature-256', '')
            if not self.verify_signature(body, signature):
                response = "HTTP/1.1 401 Unauthorized\r\nContent-Type: text/plain\r\nContent-Length: 13\r\n\r\nUnauthorized"
                client_socket.sendall(response.encode())
                return
            
            # Process webhook
            webhook_data = json.loads(body)
            self.process_webhook(webhook_data)
            
            # Send success response
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 2\r\n\r\nOK"
            client_socket.sendall(response.encode())
            
        except Exception as e:
            error_response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\nContent-Length: {len(str(e))}\r\n\r\n{str(e)}"
            client_socket.sendall(error_response.encode())
    
    def process_webhook(self, data):
        """Process webhook data"""
        event_type = data.get('event_type')
        
        if event_type == 'user.created':
            print(f"New user created: {data.get('user', {}).get('email')}")
        elif event_type == 'payment.completed':
            print(f"Payment completed: {data.get('payment', {}).get('amount')}")
        else:
            print(f"Unknown event type: {event_type}")

# Usage
webhook_receiver = WebhookReceiver("your-secret-key")
routes = {("POST", "/webhook"): webhook_receiver.handle_webhook}
start_http_server("127.0.0.1", 8080, routes=routes)
```

## Error Handling

### Client Error Handling

```python
from kn_sock import http_get
import socket

def safe_http_get(host, port, path, headers=None):
    """Safely make HTTP GET request with error handling"""
    try:
        response = http_get(host, port, path, headers=headers)
        return response
    except socket.timeout:
        print(f"Timeout connecting to {host}:{port}")
        return None
    except ConnectionRefusedError:
        print(f"Connection refused to {host}:{port}")
        return None
    except Exception as e:
        print(f"Error making request: {e}")
        return None

# Usage
response = safe_http_get("example.com", 80, "/")
if response:
    print("Request successful")
else:
    print("Request failed")
```

### Server Error Handling

```python
from kn_sock import start_http_server

def safe_handler(request, client_socket):
    """Handler with error handling"""
    try:
        # Your handler logic here
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nHello"
        client_socket.sendall(response.encode())
    except Exception as e:
        # Send error response
        error_msg = f"Internal Server Error: {str(e)}"
        error_response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\nContent-Length: {len(error_msg)}\r\n\r\n{error_msg}"
        client_socket.sendall(error_response.encode())

routes = {("GET", "/safe"): safe_handler}
start_http_server("127.0.0.1", 8080, routes=routes)
```

## Limitations

### Current Limitations

- No support for redirects
- No support for chunked encoding
- No support for cookies
- No support for HTTP/2
- Limited header parsing
- No support for streaming responses

### Workarounds

For advanced HTTP features, consider using a full HTTP library like `requests` or `httpx`:

```python
import requests

# For complex HTTP operations
response = requests.get("https://api.example.com/users", 
                       headers={"Authorization": "Bearer token"},
                       timeout=30)
data = response.json()
```

## Best Practices

### Security

1. **Always validate input** in server handlers
2. **Use HTTPS** for sensitive data
3. **Implement proper authentication** for APIs
4. **Validate file uploads** to prevent security issues
5. **Use proper error handling** to avoid information leakage

### Performance

1. **Use connection pooling** for multiple requests
2. **Implement caching** for static content
3. **Compress responses** for large data
4. **Use async operations** for high concurrency

### Reliability

1. **Implement retry logic** for failed requests
2. **Use timeouts** to prevent hanging connections
3. **Handle network errors** gracefully
4. **Log errors** for debugging

## Related Topics

- **[TCP Protocol](../protocols/tcp.md)** - For underlying transport
- **[Secure TCP](../protocols/secure-tcp.md)** - For HTTPS functionality
- **[API Reference](../api-reference.md)** - For complete function documentation 