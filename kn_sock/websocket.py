import socket
import threading
import base64
import hashlib
import struct
from typing import Callable, Optional, Dict
import asyncio

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


class WebSocketConnection:
    """
    Represents a synchronous WebSocket connection.

    Used for sending and receiving UTF-8 text messages after a successful
    WebSocket handshake. Typically returned by `connect_websocket()` or passed to
    handlers in `start_websocket_server()`.

    Methods:
        send(str): Send a UTF-8 text message.
        recv(): Receive a UTF-8 message.
        close(): Gracefully close the connection.

    Attributes:
        conn (socket.socket): The underlying socket object.
        addr (tuple): Remote address of the peer.
        open (bool): True if the connection is active.
    """
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.open = True

    def send(self, message: str):
        """
        Send a UTF-8 text message over the WebSocket connection.

        Args:
            message (str): The message to send.

        Raises:
            socket.error: If the send operation fails.
            BrokenPipeError: If the connection is already closed.

        Example:
            >>> ws.send("Hello from client")
        """    
        # Send a text frame
        payload = message.encode("utf-8")
        header = b"\x81"  # FIN + text frame
        length = len(payload)
        if length < 126:
            header += struct.pack("B", length)
        elif length < (1 << 16):
            header += struct.pack("!BH", 126, length)
        else:
            header += struct.pack("!BQ", 127, length)
        self.conn.sendall(header + payload)

    def recv(self) -> str:
        """
        Receive a UTF-8 text message from the WebSocket connection.

        Returns:
            str: The received message, or an empty string if the connection is closed.

        Raises:
            socket.error: If receiving fails.
            UnicodeDecodeError: If the received message is not valid UTF-8.

        Example:
            >>> message = ws.recv()
            >>> print(message)
        """
        # Receive a text frame (no fragmentation, no extensions)
        first2 = self.conn.recv(2)
        if not first2:
            self.open = False
            return ""
        fin_opcode, mask_len = first2
        masked = mask_len & 0x80
        length = mask_len & 0x7F
        if length == 126:
            length = struct.unpack("!H", self.conn.recv(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self.conn.recv(8))[0]
        if masked:
            mask = self.conn.recv(4)
            data = bytearray(self.conn.recv(length))
            for i in range(length):
                data[i] ^= mask[i % 4]
            return data.decode("utf-8")
        else:
            data = self.conn.recv(length)
            return data.decode("utf-8")

    def close(self):
        """
        Close the WebSocket connection gracefully.

        Sends a close frame and closes the socket.

        Raises:
            socket.error: If the socket fails to send the close frame.

        Example:
            >>> ws.close()
        """
        # Send close frame
        try:
            self.conn.sendall(b"\x88\x00")
        except Exception:
            pass
        self.conn.close()
        self.open = False


def _handshake(conn):
    """
    Perform a minimal WebSocket handshake on the given TCP socket.

    Args:
        conn (socket.socket): The client socket.

    Returns:
        bool: True if the handshake succeeded, False otherwise.
    
    Example:
    This function is used internally by `start_websocket_server()`.

    >>> if not _handshake(conn):
    ...     conn.close()
    """
    # Minimal WebSocket handshake
    request = b""
    while b"\r\n\r\n" not in request:
        chunk = conn.recv(1024)
        if not chunk:
            return False
        request += chunk
    headers = {}
    for line in request.decode().split("\r\n")[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            headers[k.lower()] = v
    key = headers.get("sec-websocket-key")
    if not key:
        return False
    accept = base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode()
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept}\r\n\r\n"
    )
    conn.sendall(response.encode())
    return True


def start_websocket_server(
    host: str,
    port: int,
    handler: Callable[[WebSocketConnection], None],
    shutdown_event=None,
):
    """
    Start a blocking WebSocket server using threads per client.

    Accepts TCP connections, performs a WebSocket handshake, and passes each
    connected client to the given handler in a new thread.

    Args:
        host (str): Bind address (e.g. "0.0.0.0").
        port (int): Port number to listen on.
        handler (Callable): Function that receives a WebSocketConnection.
        shutdown_event (threading.Event, optional): Allows graceful shutdown if set.

    Raises:
        OSError: If the socket cannot bind or listen.
        socket.error: On lower-level socket failure.

    Example:
        >>> def echo(ws):
        ...     while ws.open:
        ...         msg = ws.recv()
        ...         ws.send(f"Echo: {msg}")
        >>> start_websocket_server("0.0.0.0", 8765, echo)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print(f"[WebSocket][SERVER] Listening on {host}:{port}")
    try:
        while True:
            if shutdown_event is not None and shutdown_event.is_set():
                print("[WebSocket][SERVER] Shutdown event set. Stopping server.")
                break
            sock.settimeout(1.0)
            try:
                conn, addr = sock.accept()
            except socket.timeout:
                continue
            if not _handshake(conn):
                conn.close()
                continue
            ws = WebSocketConnection(conn, addr)
            threading.Thread(target=handler, args=(ws,), daemon=True).start()
    finally:
        sock.close()
        print("[WebSocket][SERVER] Shutdown complete.")


def connect_websocket(
    host: str, port: int, resource: str = "/", headers: Optional[dict] = None
) -> WebSocketConnection:
    """
    Connect to a WebSocket server synchronously.

    Performs a WebSocket handshake and returns a WebSocketConnection.

    Args:
        host (str): Server hostname or IP.
        port (int): Port number.
        resource (str): URL path to connect to (default is "/").
        headers (dict, optional): Additional HTTP headers.

    Returns:
        WebSocketConnection: A usable connection object.

    Raises:
        ConnectionError: If the handshake fails.
        socket.error: If the connection fails.

    Example:
        >>> ws = connect_websocket("localhost", 8765)
        >>> ws.send("hello")
        >>> print(ws.recv())
        >>> ws.close()
    """
    import os
    import random

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    key = base64.b64encode(os.urandom(16)).decode()
    req = (
        f"GET {resource} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
    )
    if headers:
        for k, v in headers.items():
            req += f"{k}: {v}\r\n"
    req += "\r\n"
    sock.sendall(req.encode())
    # Read response
    resp = b""
    while b"\r\n\r\n" not in resp:
        chunk = sock.recv(1024)
        if not chunk:
            raise ConnectionError("WebSocket handshake failed")
        resp += chunk
    if b"101" not in resp.split(b"\r\n", 1)[0]:
        raise ConnectionError("WebSocket handshake failed")
    return WebSocketConnection(sock, (host, port))


# --- Async WebSocket Client ---
class AsyncWebSocketConnection:
    """
    Represents an asynchronous WebSocket connection.

    Used for sending and receiving UTF-8 text messages in asyncio-based clients.

    Methods:
        send(str): Send a message asynchronously.
        recv(): Receive a message asynchronously.
        close(): Gracefully close the connection.

    Attributes:
        reader (asyncio.StreamReader): The input stream.
        writer (asyncio.StreamWriter): The output stream.
        open (bool): True if the connection is still open.
    """
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.open = True

    async def send(self, message: str):
        """
        Send a UTF-8 text message asynchronously.

        Args:
            message (str): Message to send.

        Raises:
            ConnectionError: If the socket write fails.

        Example:
            >>> await ws.send("Hello async WebSocket")
        """
        payload = message.encode("utf-8")
        header = b"\x81"
        length = len(payload)
        if length < 126:
            header += struct.pack("B", length)
        elif length < (1 << 16):
            header += struct.pack("!BH", 126, length)
        else:
            header += struct.pack("!BQ", 127, length)
        self.writer.write(header + payload)
        await self.writer.drain()

    async def recv(self) -> str:
        """
        Receive a UTF-8 text message asynchronously.

        Returns:
            str: The received message, or an empty string on disconnect.

        Raises:
            asyncio.IncompleteReadError: If the socket closes mid-frame.
            UnicodeDecodeError: If the message cannot be decoded.

        Example:
            >>> message = await ws.recv()
            >>> print(message)
        """
        first2 = await self.reader.readexactly(2)
        if not first2:
            self.open = False
            return ""
        fin_opcode, mask_len = first2
        masked = mask_len & 0x80
        length = mask_len & 0x7F
        if length == 126:
            length = struct.unpack("!H", await self.reader.readexactly(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", await self.reader.readexactly(8))[0]
        if masked:
            mask = await self.reader.readexactly(4)
            data = bytearray(await self.reader.readexactly(length))
            for i in range(length):
                data[i] ^= mask[i % 4]
            return data.decode("utf-8")
        else:
            data = await self.reader.readexactly(length)
            return data.decode("utf-8")

    async def close(self):
        """
        Close the asynchronous WebSocket connection gracefully.

        Sends a close frame and closes the writer stream.

        Raises:
            ConnectionError: If the writer fails to send the close frame.

        Example:
            >>> await ws.close()
        """
        try:
            self.writer.write(b"\x88\x00")
            await self.writer.drain()
        except Exception:
            pass
        self.writer.close()
        self.open = False


async def async_connect_websocket(
    host: str, port: int, resource: str = "/", headers: Optional[Dict[str, str]] = None
) -> AsyncWebSocketConnection:
    """
    Connect to a WebSocket server asynchronously.

    Performs a WebSocket handshake and returns an AsyncWebSocketConnection.

    Args:
        host (str): Server hostname or IP.
        port (int): Port number.
        resource (str): Path component (default is "/").
        headers (dict, optional): Additional handshake headers.

    Returns:
        AsyncWebSocketConnection: A usable async connection object.

    Raises:
        ConnectionError: If the handshake fails.
        asyncio.CancelledError: If the coroutine is cancelled mid-connection.

    Example:
        >>> ws = await async_connect_websocket("localhost", 8765)
        >>> await ws.send("ping")
        >>> print(await ws.recv())
        >>> await ws.close()
    """
    import os

    reader, writer = await asyncio.open_connection(host, port)
    key = base64.b64encode(os.urandom(16)).decode()
    req = (
        f"GET {resource} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
    )
    if headers:
        for k, v in headers.items():
            req += f"{k}: {v}\r\n"
    req += "\r\n"
    writer.write(req.encode())
    await writer.drain()
    resp = b""
    while b"\r\n\r\n" not in resp:
        chunk = await reader.read(1024)
        if not chunk:
            raise ConnectionError("WebSocket handshake failed")
        resp += chunk
    if b"101" not in resp.split(b"\r\n", 1)[0]:
        raise ConnectionError("WebSocket handshake failed")
    return AsyncWebSocketConnection(reader, writer)
