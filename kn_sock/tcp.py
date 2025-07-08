# kn_sock/tcp.py

import socket
import threading
import asyncio
from typing import Callable, Awaitable
import ssl
import queue
import time

BUFFER_SIZE = 1024

def _get_socket_family(host):
    # Return AF_INET6 if host is IPv6, else AF_INET
    if ':' in host:
        return socket.AF_INET6
    return socket.AF_INET

# -----------------------------
# 🖥️ TCP Server (Synchronous)
# -----------------------------

def start_tcp_server(port: int, handler_func: Callable[[bytes, tuple, socket.socket], None], host: str = '0.0.0.0', shutdown_event=None):
    """
    Starts a synchronous TCP server (IPv4/IPv6 supported).
    Args:
        port (int): Port to bind.
        handler_func (callable): Function to handle (data, addr, client_socket).
        host (str): Host to bind (IPv4 or IPv6).
        shutdown_event (threading.Event, optional): If provided, server will exit when event is set.
    """
    family = _get_socket_family(host)
    server_socket = socket.socket(family, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[TCP] Server listening on {host}:{port}")

    while True:
        if shutdown_event is not None and shutdown_event.is_set():
            print("[TCP] Shutdown event set. Stopping server.")
            break
        try:
            server_socket.settimeout(1.0)
            client_socket, addr = server_socket.accept()
        except socket.timeout:
            continue
        print(f"[TCP] Connection from {addr}")
        data = client_socket.recv(BUFFER_SIZE)
        if data:
            handler_func(data, addr, client_socket)
        client_socket.close()
    server_socket.close()

# -----------------------------
# 🧵 Threaded TCP Server
# -----------------------------

def start_threaded_tcp_server(port: int, handler_func: Callable[[bytes, tuple, socket.socket], None], host: str = '0.0.0.0', shutdown_event=None):
    """
    Starts a threaded TCP server (IPv4/IPv6 supported).
    Args:
        port (int): Port to bind.
        handler_func (callable): Function to handle (data, addr, client_socket).
        host (str): Host to bind (IPv4 or IPv6).
        shutdown_event (threading.Event, optional): If provided, server will exit when event is set.
    """
    family = _get_socket_family(host)
    server_socket = socket.socket(family, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print(f"[TCP] Threaded server listening on {host}:{port}")

    client_threads = []

    def client_thread(client_socket, addr):
        print(f"[TCP] Client thread started for {addr}")
        try:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                handler_func(data, addr, client_socket)
        except ConnectionResetError:
            print(f"[TCP] Connection lost from {addr}")
        finally:
            client_socket.close()
            print(f"[TCP] Connection closed for {addr}")

    try:
        while True:
            if shutdown_event is not None and shutdown_event.is_set():
                print("[TCP] Shutdown event set. Stopping threaded server.")
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
        print("[TCP] Threaded server shutdown complete.")

# -----------------------------
# 📤 TCP Client (Sync)
# -----------------------------

def send_tcp_message(host: str, port: int, message: str):
    """
    Sends a message to a TCP server (IPv4/IPv6 supported).
    """
    family = _get_socket_family(host)
    with socket.socket(family, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(message.encode('utf-8'))
        try:
            response = client_socket.recv(BUFFER_SIZE)
            print(f"[TCP] Server response: {response.decode('utf-8')}")
        except:
            pass

def send_tcp_bytes(host: str, port: int, data: bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(data)
        try:
            response = client_socket.recv(BUFFER_SIZE)
            print(f"[TCP] Server response: {response}")
        except:
            pass

# -----------------------------
# ⚡ Async TCP Server
# -----------------------------

async def start_async_tcp_server(
    port: int,
    handler_func: Callable[[bytes, tuple, asyncio.StreamWriter], Awaitable[None]],
    host: str = '0.0.0.0',
    shutdown_event: 'asyncio.Event' = None
):
    """
    Starts an asynchronous TCP server with graceful shutdown support.
    Args:
        port (int): Port to bind.
        handler_func (callable): async function (data, addr, writer).
        host (str): Host to bind.
        shutdown_event (asyncio.Event, optional): If provided, server will exit when event is set.
    """
    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        print(f"[TCP][ASYNC] Connection from {addr}")
        try:
            while True:
                data = await reader.read(BUFFER_SIZE)
                if not data:
                    break
                await handler_func(data, addr, writer)
        except Exception as e:
            print(f"[TCP][ASYNC] Error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            print(f"[TCP][ASYNC] Connection closed from {addr}")

    server = await asyncio.start_server(handle_client, host, port)
    print(f"[TCP][ASYNC] Async server listening on {host}:{port}")
    async with server:
        if shutdown_event is not None:
            await shutdown_event.wait()
            print("[TCP][ASYNC] Shutdown event set. Stopping async server.")
        else:
            await server.serve_forever()
    print("[TCP][ASYNC] Async server shutdown complete.")

# -----------------------------
# ⚡ Async TCP Client
# -----------------------------

async def send_tcp_message_async(host: str, port: int, message: str):
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(message.encode('utf-8'))
    await writer.drain()
    try:
        data = await reader.read(BUFFER_SIZE)
        print(f"[TCP][ASYNC] Server says: {data.decode('utf-8')}")
    except:
        pass
    writer.close()
    await writer.wait_closed()

def start_ssl_tcp_server(port, handler_func, certfile, keyfile, cafile=None, require_client_cert=False, host='0.0.0.0', shutdown_event=None):
    """
    Starts a synchronous SSL/TLS TCP server with graceful shutdown support.
    Args:
        port (int): Port to bind.
        handler_func (callable): Function to handle (data, addr, client_socket).
        certfile (str): Path to server certificate (PEM).
        keyfile (str): Path to server private key (PEM).
        cafile (str, optional): CA cert for client cert verification.
        require_client_cert (bool): Require client certificate (mutual TLS).
        host (str): Host to bind.
        shutdown_event (threading.Event, optional): If provided, server will exit when event is set.
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
    print(f"[SSL][TCP] Server listening on {host}:{port}")
    while True:
        if shutdown_event is not None and shutdown_event.is_set():
            print("[SSL][TCP] Shutdown event set. Stopping server.")
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
            print(f"[SSL][TCP] SSL error: {e}")
        finally:
            try:
                ssl_sock.close()
            except Exception:
                pass
    server_socket.close()

def send_ssl_tcp_message(host, port, message, cafile=None, certfile=None, keyfile=None, verify=True):
    """
    Sends a message to an SSL/TLS TCP server and prints the response.
    Args:
        host (str): Server host.
        port (int): Server port.
        message (str): Message to send.
        cafile (str, optional): CA cert for server verification.
        certfile (str, optional): Client cert for mutual TLS.
        keyfile (str, optional): Client key for mutual TLS.
        verify (bool): Whether to verify server cert.
    """
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cafile)
    if not verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    if certfile and keyfile:
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host if verify else None) as ssock:
            ssock.sendall(message.encode('utf-8'))
            try:
                response = ssock.recv(BUFFER_SIZE)
                print(f"[SSL][TCP] Server response: {response.decode('utf-8')}")
            except Exception:
                pass

async def start_async_ssl_tcp_server(
    port,
    handler_func,
    certfile,
    keyfile,
    cafile=None,
    require_client_cert=False,
    host='0.0.0.0',
    shutdown_event=None
):
    """
    Starts an asynchronous SSL/TLS TCP server with graceful shutdown support.
    Args:
        port (int): Port to bind.
        handler_func (callable): async function (data, addr, writer).
        certfile (str): Path to server certificate (PEM).
        keyfile (str): Path to server private key (PEM).
        cafile (str, optional): CA cert for client cert verification.
        require_client_cert (bool): Require client certificate (mutual TLS).
        host (str): Host to bind.
        shutdown_event (asyncio.Event, optional): If provided, server will exit when event is set.
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
        addr = writer.get_extra_info('peername')
        print(f"[SSL][TCP][ASYNC] Connection from {addr}")
        try:
            while True:
                data = await reader.read(BUFFER_SIZE)
                if not data:
                    break
                await handler_func(data, addr, writer)
        except Exception as e:
            print(f"[SSL][TCP][ASYNC] Error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            print(f"[SSL][TCP][ASYNC] Connection closed from {addr}")

    server = await asyncio.start_server(
        handle_client, host, port, ssl=context
    )
    print(f"[SSL][TCP][ASYNC] Async SSL server listening on {host}:{port}")
    async with server:
        if shutdown_event is not None:
            await shutdown_event.wait()
            print("[SSL][TCP][ASYNC] Shutdown event set. Stopping async SSL server.")
        else:
            await server.serve_forever()
    print("[SSL][TCP][ASYNC] Async SSL server shutdown complete.")

async def send_ssl_tcp_message_async(
    host,
    port,
    message,
    cafile=None,
    certfile=None,
    keyfile=None,
    verify=True
):
    """
    Sends a message to an SSL/TLS TCP server asynchronously and prints the response.
    Args:
        host (str): Server host.
        port (int): Server port.
        message (str): Message to send.
        cafile (str, optional): CA cert for server verification.
        certfile (str, optional): Client cert for mutual TLS.
        keyfile (str, optional): Client key for mutual TLS.
        verify (bool): Whether to verify server cert.
    """
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cafile)
    if not verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    if certfile and keyfile:
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    reader, writer = await asyncio.open_connection(host, port, ssl=context, server_hostname=host if verify else None)
    writer.write(message.encode('utf-8'))
    await writer.drain()
    try:
        data = await reader.read(BUFFER_SIZE)
        print(f"[SSL][TCP][ASYNC] Server says: {data.decode('utf-8')}")
    except Exception:
        pass
    writer.close()
    await writer.wait_closed()

class TCPConnectionPool:
    """
    A simple thread-safe TCP (and SSL) connection pool.
    Usage:
        pool = TCPConnectionPool(host, port, max_size=2, idle_timeout=5, ssl=False, cafile=None, certfile=None, keyfile=None, verify=True)
        with pool.connection() as conn:
            conn.sendall(b"hello")
            data = conn.recv(1024)
        pool.closeall()
    """
    def __init__(self, host, port, max_size=5, idle_timeout=30, ssl=False, cafile=None, certfile=None, keyfile=None, verify=True):
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
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.cafile)
            if not self.verify:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            if self.certfile and self.keyfile:
                context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
            s = context.wrap_socket(s, server_hostname=self.host if self.verify else None)
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
            self._pool = [(c, t) for (c, t) in self._pool if now - t < self.idle_timeout]
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
                    self._pool = [(c, t) for (c, t) in self._pool if now - t < self.idle_timeout]
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
