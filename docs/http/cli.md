# HTTP: Using the CLI

## CLI Commands

### 1. Start a Minimal HTTP Server

Spin up a simple HTTP server that serves static files and custom routes (for development/testing).

| Command                 | Description                     |
|-------------------------|---------------------------------|
| `run-http-server <port>`| Start HTTP server on given port |

**Example**
```bash
docker-compose run --rm knsock run-http-server 8000
# Or: knsock run-http-server 8000
```

Output

```csharp
[HTTP][SYNC] Serving on 0.0.0.0:8000
```

### 2. HTTP GET Request
Send a GET request to an HTTP server.

| Command | Description |
|---------|-------------|
| `http-get <host> <port> <path>` | HTTP GET to endpoint |

**Example**

```bash
docker-compose run --rm knsock http-get 172.18.0.2 8000 /
```

Output

```csharp
[HTTP][CLIENT] GET http://172.18.0.2:8000/
HTTP/1.1 200 OK
...
<response body>
```

### 3. HTTP POST Request
Send a POST request (with string data) to an HTTP server.

| Command | Description |
|---------|-------------|
| `http-post <host> <port> <path> <data>` | HTTP POST to endpoint |

**Example**

```bash
docker-compose run --rm knsock http-post 172.18.0.2 8000 / "test=ok"
```

Output

```csharp
[HTTP][CLIENT] POST http://172.18.0.2:8000/
HTTP/1.1 200 OK
...
<response body>
```

### 4. HTTPS GET/POST Requests
Same as above, but with HTTPS.

| Command | Description |
|---------|-------------|
| `https-get <host> <port> <path>` | HTTPS GET to endpoint |
| `https-post <host> <port> <path> <data>` | HTTPS POST to endpoint |

### Options
| Option | Description |
|--------|-------------|
| `<port>` | Port number for server/client |
| `<host>` | IP or hostname of server |
| `<path>` | Path for GET/POST (for example, /) |
| `<data>` | Data to POST (as a string) |

### Related Topics

* **[Python API](python-api.md)**
* **[Reference](reference.md)**
* **[Testing & Troubleshooting](testing.md)**