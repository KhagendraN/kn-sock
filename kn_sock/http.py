import socket
import ssl
import os
import threading
from typing import Optional, Dict, Callable


def http_get(
    host: str, port: int = 80, path: str = "/", headers: Optional[Dict[str, str]] = None
) -> str:
    """Send a synchronous HTTP **GET** request.

    Args:
        host: Server hostname or IP address.
        port: Server port; defaults to ``80``.
        path: Resource path, for example ``"/api"`` or ``"/"``.
        headers: Optional additional request headers.

    Returns:
        str: Response body decoded as UTF-8 (errors replaced).

    Raises:
        ConnectionError: When the socket cannot connect.
        socket.error: For lower-level network errors.

    Example:
        >>> body = http_get("example.com", 80, "/")
        >>> print(body)
    """
    sock = socket.create_connection((host, port))
    req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n"
    if headers:
        for k, v in headers.items():
            req += f"{k}: {v}\r\n"
    req += "\r\n"
    sock.sendall(req.encode())
    resp = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        resp += chunk
    sock.close()
    return resp.split(b"\r\n\r\n", 1)[-1].decode(errors="replace")


def http_post(
    host: str,
    port: int = 80,
    path: str = "/",
    data: str = "",
    headers: Optional[Dict[str, str]] = None,
) -> str:
    """Send a synchronous HTTP **POST** request with a string payload.

    Args:
        host: Server hostname or IP address.
        port: Server port; defaults to ``80``.
        path: Resource path.
        data: Request body as a string.
        headers: Optional additional request headers.

    Returns:
        str: Response body decoded as UTF-8 (errors replaced).

    Raises:
        ConnectionError: When the socket cannot connect.
        socket.error: For lower-level network errors.

    Example:
        >>> body = http_post("localhost", 8000, "/", "name=knsock")
        >>> assert "200 OK" in body
    """
    sock = socket.create_connection((host, port))
    req = f"POST {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\nContent-Length: {len(data.encode())}\r\n"
    if headers:
        for k, v in headers.items():
            req += f"{k}: {v}\r\n"
    req += "\r\n"
    req = req.encode() + data.encode()
    sock.sendall(req)
    resp = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        resp += chunk
    sock.close()
    return resp.split(b"\r\n\r\n", 1)[-1].decode(errors="replace")


def https_get(
    host: str,
    port: int = 443,
    path: str = "/",
    headers: Optional[Dict[str, str]] = None,
    cafile: Optional[str] = None,
) -> str:
    """Send a synchronous **HTTPS GET** request.

    Args:
        host: Server hostname.
        port: Server port; defaults to ``443``.
        path: Resource path.
        headers: Optional additional request headers.
        cafile: Path to a CA bundle file to verify the server certificate.

    Returns:
        str: Response body decoded as UTF-8 (errors replaced).

    Raises:
        ConnectionError: When the socket cannot connect.
        ssl.SSLError: For TLS handshake problems.

    Example:
        >>> body = https_get("api.github.com", 443, "/")
        >>> print(body)
    """
    context = (
        ssl.create_default_context(cafile=cafile)
        if cafile
        else ssl.create_default_context()
    )
    sock = socket.create_connection((host, port))
    ssock = context.wrap_socket(sock, server_hostname=host)
    req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n"
    if headers:
        for k, v in headers.items():
            req += f"{k}: {v}\r\n"
    req += "\r\n"
    ssock.sendall(req.encode())
    resp = b""
    while True:
        chunk = ssock.recv(4096)
        if not chunk:
            break
        resp += chunk
    ssock.close()
    return resp.split(b"\r\n\r\n", 1)[-1].decode(errors="replace")


def https_post(
    host: str,
    port: int = 443,
    path: str = "/",
    data: str = "",
    headers: Optional[Dict[str, str]] = None,
    cafile: Optional[str] = None,
) -> str:
    """Send a synchronous **HTTPS POST** request with a string payload.

    Args:
        host: Server hostname.
        port: Server port; defaults to ``443``.
        path: Resource path.
        data: Request body as a string.
        headers: Optional additional request headers.
        cafile: Path to a CA bundle file to verify the server certificate.

    Returns:
        str: Response body decoded as UTF-8 (errors replaced).

    Raises:
        ConnectionError: When the socket cannot connect.
        ssl.SSLError: For TLS handshake problems.

    Example:
        >>> body = https_post("example.com", 443, "/submit", "payload")
        >>> print(body)
    """
    context = (
        ssl.create_default_context(cafile=cafile)
        if cafile
        else ssl.create_default_context()
    )
    sock = socket.create_connection((host, port))
    ssock = context.wrap_socket(sock, server_hostname=host)
    req = f"POST {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\nContent-Length: {len(data.encode())}\r\n"
    if headers:
        for k, v in headers.items():
            req += f"{k}: {v}\r\n"
    req += "\r\n"
    req = req.encode() + data.encode()
    ssock.sendall(req)
    resp = b""
    while True:
        chunk = ssock.recv(4096)
        if not chunk:
            break
        resp += chunk
    ssock.close()
    return resp.split(b"\r\n\r\n", 1)[-1].decode(errors="replace")


def start_http_server(
    host: str,
    port: int,
    static_dir: Optional[str] = None,
    routes: Optional[Dict[str, Callable]] = None,
    shutdown_event: Optional[threading.Event] = None,
):
    """Start a blocking, single-thread-per-client HTTP server.

    The server handles three simple cases:

    1. If *routes* defines a handler for ``(method, path)``, that handler runs.
       The handler must send the full HTTP response on the passed socket.
    2. If *static_dir* is set, any other path maps to ``static_dir/<path>``.
       Missing files return **404**.
    3. Any unmatched request returns **404**.

    Args:
        host: Bind address (for example ``"0.0.0.0"``).
        port: Bind port.
        static_dir: Optional directory to serve static files from.
        routes: Optional mapping of ``(method, path)`` tuples to handler
            functions.  A handler receives ``(request_dict, client_socket)``.
        shutdown_event: Optional :class:`threading.Event` that, when set,
            prompts the server loop to exit cleanly.
    
    Raises:
        OSError: If the socket fails to bind (e.g., port already in use).
        ValueError: If invalid handler arguments or routes are passed.
        RuntimeError: If a threading error occurs when starting the server.

    Example:
        ```python
        from kn_sock.http import start_http_server

        def ping(req, sock):
            sock.sendall(b"HTTP/1.1 200 OK\\r\\nContent-Length: 4\\r\\n\\r\\npong")

        start_http_server(
            host="0.0.0.0",
            port=8080,
            routes={("GET", "/ping"): ping}
        )
        ```
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print(f"[HTTP][SERVER] Listening on {host}:{port}")

    def serve_client(client_sock, addr):
        try:
            req = b""
            while b"\r\n\r\n" not in req:
                chunk = client_sock.recv(1024)
                if not chunk:
                    break
                req += chunk
            if not req:
                client_sock.close()
                return
            lines = req.decode(errors="replace").split("\r\n")
            request_line = lines[0]
            method, path, _ = request_line.split(" ", 2)
            headers = {}
            for line in lines[1:]:
                if ": " in line:
                    k, v = line.split(": ", 1)
                    headers[k.lower()] = v
                if line == "":
                    break
            # Route handler
            if routes and (method, path) in routes:
                request = {
                    "method": method,
                    "path": path,
                    "headers": headers,
                    "raw": req,
                }
                routes[(method, path)](request, client_sock)
                client_sock.close()
                return
            # Static file
            if static_dir:
                rel_path = path.lstrip("/") or "index.html"
                file_path = os.path.join(static_dir, rel_path)
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as f:
                        content = f.read()
                    client_sock.sendall(
                        b"HTTP/1.1 200 OK\r\nContent-Length: "
                        + str(len(content)).encode()
                        + b"\r\n\r\n"
                        + content
                    )
                else:
                    client_sock.sendall(
                        b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
                    )
            else:
                client_sock.sendall(
                    b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
                )
        except Exception as e:
            try:
                client_sock.sendall(
                    b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"
                )
            except Exception:
                pass
        finally:
            client_sock.close()

    try:
        while True:
            if shutdown_event is not None and shutdown_event.is_set():
                print("[HTTP][SERVER] Shutdown event set. Stopping server.")
                break
            sock.settimeout(1.0)
            try:
                client_sock, addr = sock.accept()
            except socket.timeout:
                continue
            threading.Thread(
                target=serve_client, args=(client_sock, addr), daemon=True
            ).start()
    finally:
        sock.close()
        print("[HTTP][SERVER] Shutdown complete.")
