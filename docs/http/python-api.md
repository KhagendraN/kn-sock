# HTTP Python API

Use the kn‑sock Python API to launch lightweight HTTP servers and issue GET/POST requests directly in code.

## Start an HTTP Server

```python
from kn_sock import start_http_server

def hello_handler(request, sock):
    sock.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello")

start_http_server(
    host="0.0.0.0",
    port=8000,
    routes={("GET", "/hello"): hello_handler}
)
```

This starts a synchronous HTTP server that:

- Binds to 0.0.0.0:8000
- Responds to GET /hello with Hello
- Unmatched paths return 404 Not Found unless you provide a static_dir.

## Send HTTP GET / POST Requests

```python
from kn_sock import http_get, http_post

# GET request
body = http_get("localhost", 8000, "/hello")
print(body)

# POST request
body = http_post("localhost", 8000, "/", "name=knsock")
print(body)
```

Both functions return the response body as a UTF-8 decoded string. You can optionally include headers as a dict.

## Send HTTPS GET / POST Requests

```python
from kn_sock import https_get, https_post

# Basic GET request
body = https_get("example.com", 443, "/")
print(body)

# POST request with CA verification
body = https_post(
    "example.com",
    443,
    "/submit",
    "name=test",
    cafile="/etc/ssl/certs/ca-certificates.crt"
)
print(body)
```

The cafile argument is optional. If omitted, the system’s default certificate chain is used. If verification fails, an ssl.SSLError is raised.

## Example Output

**Server terminal**

```pgsql
[HTTP][SERVER] Listening on 0.0.0.0:8000
[HTTP][SERVER] GET /hello from ('127.0.0.1', 56244)
```

**Client output**

```nginx
Hello
```

## When to Use the Python API

Use the Python API when:

- You're embedding server functionality inside your application
- You want to send test requests without invoking the CLI
- You’re scripting interactions or chaining together HTTP utilities

For CLI usage, see the [CLI commands page](cli.md).

### Related Topics

* **[CLI commands](cli.md)**
* **[Reference](reference.md)**
* **[Testing & Troubleshooting](testing.md)**
