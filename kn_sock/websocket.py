import socket
import threading
import base64
import hashlib
import struct
from typing import Callable

GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

class WebSocketConnection:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.open = True

    def send(self, message: str):
        # Send a text frame
        payload = message.encode('utf-8')
        header = b'\x81'  # FIN + text frame
        length = len(payload)
        if length < 126:
            header += struct.pack('B', length)
        elif length < (1 << 16):
            header += struct.pack('!BH', 126, length)
        else:
            header += struct.pack('!BQ', 127, length)
        self.conn.sendall(header + payload)

    def recv(self) -> str:
        # Receive a text frame (no fragmentation, no extensions)
        first2 = self.conn.recv(2)
        if not first2:
            self.open = False
            return ''
        fin_opcode, mask_len = first2
        masked = mask_len & 0x80
        length = mask_len & 0x7F
        if length == 126:
            length = struct.unpack('!H', self.conn.recv(2))[0]
        elif length == 127:
            length = struct.unpack('!Q', self.conn.recv(8))[0]
        if masked:
            mask = self.conn.recv(4)
            data = bytearray(self.conn.recv(length))
            for i in range(length):
                data[i] ^= mask[i % 4]
            return data.decode('utf-8')
        else:
            data = self.conn.recv(length)
            return data.decode('utf-8')

    def close(self):
        # Send close frame
        try:
            self.conn.sendall(b'\x88\x00')
        except Exception:
            pass
        self.conn.close()
        self.open = False


def _handshake(conn):
    # Minimal WebSocket handshake
    request = b''
    while b'\r\n\r\n' not in request:
        chunk = conn.recv(1024)
        if not chunk:
            return False
        request += chunk
    headers = {}
    for line in request.decode().split('\r\n')[1:]:
        if ': ' in line:
            k, v = line.split(': ', 1)
            headers[k.lower()] = v
    key = headers.get('sec-websocket-key')
    if not key:
        return False
    accept = base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode()
    response = (
        'HTTP/1.1 101 Switching Protocols\r\n'
        'Upgrade: websocket\r\n'
        'Connection: Upgrade\r\n'
        f'Sec-WebSocket-Accept: {accept}\r\n\r\n'
    )
    conn.sendall(response.encode())
    return True


def start_websocket_server(host: str, port: int, handler: Callable[[WebSocketConnection], None], shutdown_event=None):
    """
    Start a minimal WebSocket server.
    Args:
        host (str): Host to bind.
        port (int): Port to bind.
        handler (callable): Function called with WebSocketConnection for each client.
        shutdown_event (threading.Event, optional): For graceful shutdown.
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


def connect_websocket(host: str, port: int, resource: str = '/', headers: dict = None) -> WebSocketConnection:
    """
    Connect to a WebSocket server and return a WebSocketConnection.
    Args:
        host (str): Server host.
        port (int): Server port.
        resource (str): Resource path (default '/').
        headers (dict): Additional headers.
    Returns:
        WebSocketConnection
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
    resp = b''
    while b'\r\n\r\n' not in resp:
        chunk = sock.recv(1024)
        if not chunk:
            raise ConnectionError("WebSocket handshake failed")
        resp += chunk
    if b"101" not in resp.split(b"\r\n", 1)[0]:
        raise ConnectionError("WebSocket handshake failed")
    return WebSocketConnection(sock, (host, port)) 