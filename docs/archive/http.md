# HTTP and HTTPS Utilities

kn-sock makes it easy to create minimal HTTP servers, issue GET/POST requests, and test HTTPS endpoints directly from the CLI or Python API.

## CLI Commands

### 1. Start a Minimal HTTP Server

Spin up a simple HTTP server that serves static files and custom routes (for development/testing).

| Command                           | Description                            |
|------------------------------------|----------------------------------------|
| `run-http-server <port>`           | Start HTTP server on given port        |

**Example:**
```sh
docker-compose run --rm knsock run-http-server 8000
# Or: knsock run-http-server 8000
```
**Output:**
```
[HTTP][SYNC] Serving on 0.0.0.0:8000
```

### 2. HTTP GET Request

Send a GET request to an HTTP server.

| Command                           | Description                   |
|------------------------------------|-------------------------------|
| `http-get <host> <port> <path>`   | HTTP GET to endpoint          |

**Example:**
```sh
docker-compose run --rm knsock http-get 172.18.0.2 8000 /
```
**Output:**
```
[HTTP][CLIENT] GET http://172.18.0.2:8000/
HTTP/1.1 200 OK
...
<response body>
```

### 3. HTTP POST Request

Send a POST request (with string data) to an HTTP server.

| Command                                       | Description                   |
|-----------------------------------------------|-------------------------------|
| `http-post <host> <port> <path> <data>`      | HTTP POST to endpoint         |

**Example:**
```sh
docker-compose run --rm knsock http-post 172.18.0.2 8000 / "test=ok"
```
**Output:**
```
[HTTP][CLIENT] POST http://172.18.0.2:8000/
HTTP/1.1 200 OK
...
<response body>
```

### 4. HTTPS GET/POST Requests

Same as above, but with HTTPS.

| Command                                       | Description                   |
|-----------------------------------------------|-------------------------------|
| `https-get <host> <port> <path>`             | HTTPS GET to endpoint         |
| `https-post <host> <port> <path> <data>`     | HTTPS POST to endpoint        |

#### Options Table
| Option        | Description                           |
|---------------|---------------------------------------|
| `<port>`      | Port number for server/client         |
| `<host>`      | IP or hostname of server             |
| `<path>`      | Path for GET/POST (e.g., /api, /)     |
| `<data>`      | Data to POST (as a string)           |

## Python API

### Start an HTTP Server
```python
from kn_sock import start_http_server

def my_route_handler(request):
    if request.path == "/hello":
        return (200, "text/plain", b"Hello, world!")
    return (404, "text/plain", b"Not found")

start_http_server(8000, routes={"/hello": my_route_handler})
```

### HTTP GET/POST (Client)
```python
from kn_sock import http_get, http_post

# GET request
status, headers, body = http_get("127.0.0.1", 8000, "/")

# POST request
status, headers, body = http_post("127.0.0.1", 8000, "/", "name=knsock")
```

### Sample Output
**HTTP server terminal:**
```
[HTTP][SYNC] Serving on 0.0.0.0:8000
[HTTP][SERVER] GET / from ('172.18.0.1', 55123)
```

**Client terminal:**
```
[HTTP][CLIENT] GET http://172.18.0.2:8000/
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 14

Hello, world!
```

## Known Issues & Troubleshooting
| Issue                        | Symptom/Output                              | Solution                                           |
|------------------------------|---------------------------------------------|----------------------------------------------------|
| Port already in use          | `[Errno 98] Address already in use`         | Use a different port or kill other process         |
| No response/404              | `404 Not found` or empty output             | Check route/path; static only by default           |
| HTTPS errors                 | SSL certificate errors                      | Use valid/test certs or skip verification          |
| Hostname not found           | `[Errno -2] Name or service not known`      | Use container IP for Docker setups                 |

## Testing
### Manual Test
Start server:
```sh
docker-compose run --rm knsock run-http-server 8000
```

In another terminal, run:
```sh
docker-compose run --rm knsock http-get <server-ip> 8000 /
# Example: http-get 172.18.0.2 8000 /
```

Check for 200 OK and the expected response body.