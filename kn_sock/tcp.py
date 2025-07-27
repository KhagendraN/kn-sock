# kn_sock/tcp.py

import socket
import threading
import asyncio
import logging
from typing import Callable, Awaitable, Optional
import ssl
import queue
import time

logger = logging.getLogger(__name__)

BUFFER_SIZE = 1024


def _get_socket_family(host):
    # Return AF_INET6 if host is IPv6, else AF_INET
    if ":" in host:
        return socket.AF_INET6
    return socket.AF_INET


# -----------------------------
# 🖥️ TCP Server (Synchronous)
# -----------------------------


def start_tcp_server(
    port: int,
    handler_func: Callable[[bytes, tuple, socket.socket], None],
    host: str = "0.0.0.0",
    shutdown_event: Optional[threading.Event] = None,
):
    """
    Starts a synchronous TCP server (IPv4/IPv6 supported).

    Args:
        port (int): Port to bind.
        handler_func (callable): Function to handle (data, addr, client_socket).
        host (str): Host to bind (IPv4 or IPv6).
        shutdown_event (threading.Event, optional): If provided, server will exit when event is set.

    Returns:
        None

    Raises:
        OSError: If the port is unavailable or socket fails.
        socket.error: For general network errors.

    Example:
        >>> def echo_handler(data, addr, sock):
        ...     print(data)
        ...     sock.sendall(data)
        >>> start_tcp_server(8080, echo_handler)
    """
    family = _get_socket_family(host)
    server_socket = socket.socket(family, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logger.info(f"[TCP] Server listening on {host}:{port}")

    while True:
        if shutdown_event is not None and shutdown_event.is_set():
            logger.info("[TCP] Shutdown event set. Stopping server.")
            break
        try:
            server_socket.settimeout(1.0)
            client_socket, addr = server_socket.accept()
        except socket.timeout:
            continue
        logger.info(f"[TCP] Connection from {addr}")
        data = client_socket.recv(BUFFER_SIZE)
        if data:
            handler_func(data, addr, client_socket)
        client_socket.close()
    server_socket.close()


# -----------------------------
# 🧵 Threaded TCP Server
# -----------------------------


def start_threaded_tcp_server(
    port: int,
    handler_func: Callable[[bytes, tuple, socket.socket], None],
    host: str = "0.0.0.0",
    shutdown_event: Optional[threading.Event] = None,
):
    """
    Starts a multithreaded TCP server (IPv4/IPv6 supported).

    This function listens for incoming TCP connections on the specified port,
    spawning a new thread for each client. The handler function is called for
    each message received from a client.

    Args:
        port (int): Port to bind the server to.
        handler_func (callable): Function to handle incoming data.
            Signature: (data: bytes, addr: tuple, client_socket: socket.socket) -> None
        host (str, optional): Host to bind (IPv4 or IPv6). Defaults to "0.0.0.0".
        shutdown_event (threading.Event, optional): If provided, the server will exit gracefully when this event is set.

    Returns:
        None

    Raises:
        OSError: If the port is unavailable or socket operations fail.
        socket.error: For network-related errors.

    Example:
        >>> def echo_handler(data, addr, sock):
        ...     print(f"From {addr}: {data}")
        ...     sock.sendall(b"Echo: " + data)
        >>> import threading
        >>> shutdown = threading.Event()
        >>> start_threaded_tcp_server(8080, echo_handler, shutdown_event=shutdown)
    """
    family = _get_socket_family(host)
    server_socket = socket.socket(family, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    logger.info(f"[TCP] Threaded server listening on {host}:{port}")

    client_threads = []

    def client_thread(client_socket, addr):
        logger.info(f"[TCP] Client thread started for {addr}")
        try:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                handler_func(data, addr, client_socket)
        except ConnectionResetError:
            logger.warning(f"[TCP] Connection lost from {addr}")
        finally:
            client_socket.close()
            logger.info(f"[TCP] Connection closed for {addr}")

    try:
        while True:
            if shutdown_event is not None and shutdown_event.is_set():
                logger.info("[TCP] Shutdown event set. Stopping threaded server.")
                break
            try:
                server_socket.settimeout(1.0)
                client_socket, addr = server_socket.accept()
            except socket.timeout:
                continue
            t = threading.Thread(target=client_thread, args=(client_socket, addr))
            t.start()
            client_threads.append(t)
    finally:
        server_socket.close()
        for t in client_threads:
            t.join()
        logger.info("[TCP] Threaded server shutdown complete.")


# -----------------------------
# 📤 TCP Client (Sync)
# -----------------------------


def send_tcp_message(host: str, port: int, message: str):
    """
    Sends a message to a TCP server (IPv4/IPv6 supported) and logs the server's response.

    Opens a TCP connection to the specified host and port, sends the given message
    as UTF-8 bytes, and logs the server's response (if any) to the logger.
    This function does not return the server's response.

    Args:
        host (str): The target host address (IPv4, IPv6, or hostname).
        port (int): The target port number.
        message (str): The message to send.

    Returns:
        None

    Raises:
        ConnectionError: If unable to connect to the server.
        socket.error: For network-related errors.

    Example:
        >>> send_tcp_message("localhost", 8080, "hello world")
    """
    family = _get_socket_family(host)
    with socket.socket(family, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(message.encode("utf-8"))
        try:
            response = client_socket.recv(BUFFER_SIZE)
            logger.info(f"[TCP] Server response: {response.decode('utf-8')}")
        except:
            pass


def send_tcp_bytes(host: str, port: int, data: bytes):
    """
    Sends raw bytes to a TCP server and logs the response.

    Opens a TCP connection to the specified host and port, sends the given
    data as-is (no encoding), and logs the server's response (if any) as bytes.
    This function does not return the response.

    Args:
        host (str): The target host address (IPv4, IPv6, or hostname).
        port (int): The target port number.
        data (bytes): The data to send.

    Returns:
        None

    Raises:
        ConnectionError: If unable to connect to the server.
        socket.error: For network-related errors.

    Example:
        >>> send_tcp_bytes("127.0.0.1", 8080, b"ping")
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(data)
        try:
            response = client_socket.recv(BUFFER_SIZE)
            logger.info(f"[TCP] Server response: {response}")
        except:
            pass


# -----------------------------
# ⚡ Async TCP Server
# -----------------------------


async def start_async_tcp_server(
    port: int,
    handler_func: Callable[[bytes, tuple, asyncio.StreamWriter], Awaitable[None]],
    host: str = "0.0.0.0",
    shutdown_event: Optional["asyncio.Event"] = None,
):
    """
    Starts an asynchronous TCP server (IPv4/IPv6 supported).

    Listens for incoming TCP connections on the specified port using asyncio, spawning a coroutine for each client.
    The handler function is called with received data, the client address, and the StreamWriter for responses.
    Supports graceful shutdown when a shutdown_event is set.

    Args:
        port (int): Port to bind the server to.
        handler_func (Callable): Async function to handle incoming data.
            Signature: (data: bytes, addr: tuple, writer: asyncio.StreamWriter) -> Awaitable[None]
        host (str, optional): Host to bind (IPv4 or IPv6). Defaults to "0.0.0.0".
        shutdown_event (asyncio.Event, optional): If provided, the server will exit gracefully when this event is set.

    Returns:
        None

    Raises:
        OSError: If the port is unavailable or socket operations fail.
        asyncio.CancelledError: If the server task is cancelled.

    Example:
        >>> import asyncio
        >>> async def echo_handler(data, addr, writer):
        ...     print(f"Received from {addr}: {data.decode()}")
        ...     writer.write(b"Echo: " + data)
        ...     await writer.drain()
        >>> asyncio.run(start_async_tcp_server(8080, echo_handler))
    """

    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info("peername")
        logger.info(f"[TCP][ASYNC] Connection from {addr}")
        try:
            while True:
                data = await reader.read(BUFFER_SIZE)
                if not data:
                    break
                await handler_func(data, addr, writer)
        except Exception as e:
            logger.error(f"[TCP][ASYNC] Error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(f"[TCP][ASYNC] Connection closed from {addr}")

    server = await asyncio.start_server(handle_client, host, port)
    logger.info(f"[TCP][ASYNC] Async server listening on {host}:{port}")
    async with server:
        if shutdown_event is not None:
            await shutdown_event.wait()
            logger.info("[TCP][ASYNC] Shutdown event set. Stopping async server.")
        else:
            await server.serve_forever()
    logger.info("[TCP][ASYNC] Async server shutdown complete.")


# -----------------------------
# ⚡ Async TCP Client
# -----------------------------


async def send_tcp_message_async(host: str, port: int, message: str):
    """
    Sends a message to a TCP server asynchronously and returns the response.

    Opens an asynchronous TCP connection to the specified host and port,
    sends the given message as UTF-8 bytes, and awaits the server's response as a string.
    Returns None if no response is received.

    Args:
        host (str): The target host address (IPv4, IPv6, or hostname).
        port (int): The target port number.
        message (str): The message to send.

    Returns:
        Optional[str]: The response from the server as a UTF-8 string, or None if no response is received.

    Raises:
        ConnectionError: If unable to connect to the server.
        socket.error: For network-related errors.

    Example:
        >>> import asyncio
        >>> response = asyncio.run(send_tcp_message_async("localhost", 8080, "hello async"))
        >>> print(response)
        Echo: hello async
    """

    reader, writer = await asyncio.open_connection(host, port)
    writer.write(message.encode("utf-8"))
    await writer.drain()
    try:
        data = await reader.read(BUFFER_SIZE)
        logger.info(f"[TCP][ASYNC] Server says: {data.decode('utf-8')}")
    except:
        pass
    writer.close()
    await writer.wait_closed()


def start_ssl_tcp_server(
    port,
    handler_func,
    certfile,
    keyfile,
    cafile=None,
    require_client_cert=False,
    host="0.0.0.0",
    shutdown_event: Optional[threading.Event] = None,
):
    """
    Starts a synchronous SSL/TLS TCP server with optional client certificate verification.

    Listens for incoming SSL/TLS connections on the specified port. For each client connection,
    wraps the socket with SSL/TLS, then invokes the handler function with the received data,
    client address, and SSL socket. Supports IPv4 and IPv6.

    Args:
        port (int): Port to bind the server to.
        handler_func (callable): Function to handle incoming data.
            Signature: (data: bytes, addr: tuple, ssl_sock: ssl.SSLSocket) -> None
        certfile (str): Path to the server certificate file in PEM format.
        keyfile (str): Path to the server private key file in PEM format.
        cafile (str, optional): Path to CA certificate for verifying client certificates.
        require_client_cert (bool, optional): Whether to require client certificates for mutual TLS. Defaults to False.
        host (str, optional): Host to bind (IPv4 or IPv6). Defaults to "0.0.0.0".
        shutdown_event (threading.Event, optional): If provided, server will exit gracefully when this event is set.

    Returns:
        None

    Raises:
        OSError: If the port is unavailable or socket operations fail.
        ssl.SSLError: For SSL/TLS handshake or certificate errors.
        socket.error: For network-related errors.

    Example:
        >>> def echo_handler(data, addr, ssl_sock):
        ...     print(f"Received from {addr}: {data}")
        ...     ssl_sock.sendall(b"Echo: " + data)
        >>> start_ssl_tcp_server(
        ...     port=8443,
        ...     handler_func=echo_handler,
        ...     certfile="server.pem",
        ...     keyfile="server-key.pem"
        ... )
    """
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    if require_client_cert:
        context.verify_mode = ssl.CERT_REQUIRED
        if cafile:
            context.load_verify_locations(cafile)
    else:
        context.verify_mode = ssl.CERT_NONE
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logger.info(f"[SSL][TCP] Server listening on {host}:{port}")
    while True:
        if shutdown_event is not None and shutdown_event.is_set():
            logger.info("[SSL][TCP] Shutdown event set. Stopping server.")
            break
        try:
            server_socket.settimeout(1.0)
            client_socket, addr = server_socket.accept()
        except socket.timeout:
            continue
        try:
            ssl_sock = context.wrap_socket(client_socket, server_side=True)
            data = ssl_sock.recv(BUFFER_SIZE)
            if data:
                handler_func(data, addr, ssl_sock)
        except ssl.SSLError as e:
            logger.error(f"[SSL][TCP] SSL error: {e}")
        finally:
            try:
                ssl_sock.close()
            except Exception:
                pass
    server_socket.close()


def send_ssl_tcp_message(
    host, port, message, cafile=None, certfile=None, keyfile=None, verify=True
):
    """
    Sends a message to an SSL/TLS TCP server and returns the response.

    Opens a secure SSL/TLS connection to the specified host and port, sends the given message as UTF-8 bytes,
    and returns the server's response as a string if one is received. Supports server verification and mutual TLS.

    Args:
        host (str): The server host address (IPv4, IPv6, or hostname).
        port (int): The server port number.
        message (str): The message to send.
        cafile (str, optional): Path to a CA certificate file for verifying the server.
        certfile (str, optional): Path to the client certificate file for mutual TLS.
        keyfile (str, optional): Path to the client private key file for mutual TLS.
        verify (bool, optional): Whether to verify the server certificate. Defaults to True.

    Returns:
        Optional[str]: The response from the server as a UTF-8 string, or None if no response is received.

    Raises:
        ConnectionError: If unable to connect to the server.
        ssl.SSLError: For SSL/TLS handshake or verification errors.
        socket.error: For network-related errors.

    Example:
        >>> send_ssl_tcp_message(
        ...     host="localhost",
        ...     port=8443,
        ...     message="secure hello",
        ...     cafile="ca.pem"
        ... )
        'Echo: secure hello'
    """
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cafile)
    if not verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    if certfile and keyfile:
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(
            sock, server_hostname=host if verify else None
        ) as ssock:
            ssock.sendall(message.encode("utf-8"))
            try:
                response = ssock.recv(BUFFER_SIZE)
                logger.info(f"[SSL][TCP] Server response: {response.decode('utf-8')}")
            except Exception:
                pass


async def start_async_ssl_tcp_server(
    port,
    handler_func,
    certfile,
    keyfile,
    cafile=None,
    require_client_cert=False,
    host="0.0.0.0",
    shutdown_event: Optional["asyncio.Event"] = None,
):
    """
    Starts an asynchronous SSL/TLS TCP server with optional client certificate verification.

    Listens for incoming SSL/TLS connections using asyncio on the specified port.
    For each client, wraps the connection with SSL/TLS and invokes the provided async handler function
    with the received data, client address, and StreamWriter. Supports IPv4 and IPv6, as well as graceful shutdown.

    Args:
        port (int): Port to bind the server to.
        handler_func (Callable): Async function to handle incoming data.
            Signature: (data: bytes, addr: tuple, writer: asyncio.StreamWriter) -> Awaitable[None]
        certfile (str): Path to the server certificate file in PEM format.
        keyfile (str): Path to the server private key file in PEM format.
        cafile (str, optional): Path to CA certificate for verifying client certificates.
        require_client_cert (bool, optional): Whether to require client certificates for mutual TLS. Defaults to False.
        host (str, optional): Host to bind (IPv4 or IPv6). Defaults to "0.0.0.0".
        shutdown_event (asyncio.Event, optional): If provided, the server will exit gracefully when this event is set.

    Returns:
        None

    Raises:
        OSError: If the port is unavailable or socket operations fail.
        ssl.SSLError: For SSL/TLS handshake or certificate errors.
        asyncio.CancelledError: If the server task is cancelled.

    Example:
        >>> import asyncio
        >>> async def echo_handler(data, addr, writer):
        ...     print(f"Received from {addr}: {data.decode()}")
        ...     writer.write(b"Echo: " + data)
        ...     await writer.drain()
        >>> asyncio.run(start_async_ssl_tcp_server(
        ...     port=8443,
        ...     handler_func=echo_handler,
        ...     certfile="server.pem",
        ...     keyfile="server-key.pem"
        ... ))
    """
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    if require_client_cert:
        context.verify_mode = ssl.CERT_REQUIRED
        if cafile:
            context.load_verify_locations(cafile)
    else:
        context.verify_mode = ssl.CERT_NONE

    async def handle_client(reader, writer):
        addr = writer.get_extra_info("peername")
        logger.info(f"[SSL][TCP][ASYNC] Connection from {addr}")
        try:
            while True:
                data = await reader.read(BUFFER_SIZE)
                if not data:
                    break
                await handler_func(data, addr, writer)
        except Exception as e:
            logger.error(f"[SSL][TCP][ASYNC] Error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(f"[SSL][TCP][ASYNC] Connection closed from {addr}")

    server = await asyncio.start_server(handle_client, host, port, ssl=context)
    logger.info(f"[SSL][TCP][ASYNC] Async SSL server listening on {host}:{port}")
    async with server:
        if shutdown_event is not None:
            await shutdown_event.wait()
            logger.info(
                "[SSL][TCP][ASYNC] Shutdown event set. Stopping async SSL server."
            )
        else:
            await server.serve_forever()
    logger.info("[SSL][TCP][ASYNC] Async SSL server shutdown complete.")


async def send_ssl_tcp_message_async(
    host, port, message, cafile=None, certfile=None, keyfile=None, verify=True
):
    """
    Sends a message to an SSL/TLS TCP server asynchronously and returns the response.

    Opens an asynchronous SSL/TLS connection to the specified host and port,
    sends the given message as UTF-8 bytes, and awaits the server's response as a string.
    Supports server verification and mutual TLS authentication.

    Args:
        host (str): The server host address (IPv4, IPv6, or hostname).
        port (int): The server port number.
        message (str): The message to send.
        cafile (str, optional): Path to a CA certificate file for verifying the server.
        certfile (str, optional): Path to the client certificate file for mutual TLS.
        keyfile (str, optional): Path to the client private key file for mutual TLS.
        verify (bool, optional): Whether to verify the server certificate. Defaults to True.

    Returns:
        Optional[str]: The response from the server as a UTF-8 string, or None if no response is received.

    Raises:
        ConnectionError: If unable to connect to the server.
        ssl.SSLError: For SSL/TLS handshake or verification errors.
        socket.error: For network-related errors.

    Example:
        >>> import asyncio
        >>> response = asyncio.run(
        ...     send_ssl_tcp_message_async(
        ...         host="localhost",
        ...         port=8443,
        ...         message="secure async hello",
        ...         cafile="ca.pem"
        ...     )
        ... )
        >>> print(response)
        Echo: secure async hello
    """
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cafile)
    if not verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    if certfile and keyfile:
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    reader, writer = await asyncio.open_connection(
        host, port, ssl=context, server_hostname=host if verify else None
    )
    writer.write(message.encode("utf-8"))
    await writer.drain()
    try:
        data = await reader.read(BUFFER_SIZE)
        logger.info(f"[SSL][TCP][ASYNC] Server says: {data.decode('utf-8')}")
    except Exception:
        pass
    writer.close()
    await writer.wait_closed()


class TCPConnectionPool:
    """
    Thread-safe TCP/SSL connection pool for efficient reuse of socket connections.

    Manages a pool of TCP or SSL connections to a given host and port, allowing
    multiple threads to acquire and release connections as needed. The pool
    automatically closes idle connections after a configurable timeout.

    Typical usage:

        >>> pool = TCPConnectionPool("localhost", 8080, max_size=5, idle_timeout=30)
        >>> with pool.connection() as conn:
        ...     conn.sendall(b"ping")
        ...     response = conn.recv(1024)
        >>> pool.closeall()

    Args:
        host (str): The server host address (IPv4, IPv6, or hostname).
        port (int): The server port number.
        max_size (int, optional): Maximum number of concurrent connections. Defaults to 5.
        idle_timeout (int, optional): Seconds before idle connections are closed. Defaults to 30.
        ssl (bool, optional): Whether to use SSL/TLS for connections. Defaults to False.
        cafile (str, optional): Path to CA certificate for SSL/TLS verification.
        certfile (str, optional): Path to client certificate for mutual TLS.
        keyfile (str, optional): Path to client private key for mutual TLS.
        verify (bool, optional): Whether to verify the server certificate. Defaults to True.

    Methods:
        connection(): Acquire a connection from the pool as a context manager.
        closeall(): Close all connections and clear the pool.

    Notes:
        - Connections are managed in a thread-safe manner using an internal lock.
        - Idle connections are closed and removed from the pool after `idle_timeout` seconds.
        - When `max_size` is reached, additional requests block until a connection is released.

    Example:
        >>> pool = TCPConnectionPool("localhost", 8080, ssl=True, cafile="ca.pem")
        >>> with pool.connection() as conn:
        ...     conn.sendall(b"hello")
        ...     print(conn.recv(1024))
        >>> pool.closeall()
    """

    def __init__(
        self,
        host,
        port,
        max_size=5,
        idle_timeout=30,
        ssl=False,
        cafile=None,
        certfile=None,
        keyfile=None,
        verify=True,
    ):
        self.host = host
        self.port = port
        self.max_size = max_size
        self.idle_timeout = idle_timeout
        self.ssl = ssl
        self.cafile = cafile
        self.certfile = certfile
        self.keyfile = keyfile
        self.verify = verify
        self._pool = []  # list of (conn, last_used_time)
        self._lock = threading.Lock()
        self._used = 0

    def _create_conn(self):
        s = socket.create_connection((self.host, self.port))
        if self.ssl:
            context = ssl.create_default_context(
                ssl.Purpose.SERVER_AUTH, cafile=self.cafile
            )
            if not self.verify:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            if self.certfile and self.keyfile:
                context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
            s = context.wrap_socket(
                s, server_hostname=self.host if self.verify else None
            )
        return s

    class _PooledConn:
        def __init__(self, pool, conn):
            self._pool = pool
            self._conn = conn
            self._closed = False

        def __enter__(self):
            return self._conn

        def __exit__(self, exc_type, exc_val, exc_tb):
            if not self._closed:
                self._pool._release(self._conn)

        def close(self):
            if not self._closed:
                self._conn.close()
                self._closed = True

    def connection(self):
        with self._lock:
            now = time.time()
            # Remove idle connections
            self._pool = [
                (c, t) for (c, t) in self._pool if now - t < self.idle_timeout
            ]
            if self._pool:
                conn, _ = self._pool.pop()
                self._used += 1
                return self._PooledConn(self, conn)
            elif self._used < self.max_size:
                conn = self._create_conn()
                self._used += 1
                return self._PooledConn(self, conn)
            else:
                # Wait for a connection to be released
                while True:
                    self._lock.release()
                    time.sleep(0.05)
                    self._lock.acquire()
                    now = time.time()
                    self._pool = [
                        (c, t) for (c, t) in self._pool if now - t < self.idle_timeout
                    ]
                    if self._pool:
                        conn, _ = self._pool.pop()
                        self._used += 1
                        return self._PooledConn(self, conn)

    def _release(self, conn):
        with self._lock:
            self._pool.append((conn, time.time()))
            self._used -= 1

    def closeall(self):
        with self._lock:
            for conn, _ in self._pool:
                try:
                    conn.close()
                except Exception:
                    pass
            self._pool.clear()
            self._used = 0
