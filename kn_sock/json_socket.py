# kn_sock/json_socket.py

import socket
import threading
import asyncio
import json
from typing import Callable, Awaitable, Optional

BUFFER_SIZE = 1024

# -----------------------------
# Helper Functions (Sync & Async)
# -----------------------------

def _recv_line(sock: socket.socket) -> bytes:
    """Receive bytes from socket until newline (sync)."""
    buffer = b''
    while True:
        chunk = sock.recv(1)
        if not chunk:
            break
        buffer += chunk
        if chunk == b'\n':
            break
    return buffer

async def _recv_line_async(reader: asyncio.StreamReader) -> bytes:
    """Receive bytes until newline asynchronously."""
    data = await reader.readline()
    return data

# -----------------------------
# Sync JSON Server
# -----------------------------

def start_json_server(
    port: int,
    handler_func: Callable[[dict, tuple, socket.socket], None],
    host: str = '0.0.0.0'
):
    """
    Starts a synchronous TCP server for JSON messaging.
    Expects each JSON message to be newline-terminated.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[JSON][SYNC SERVER] Listening on {host}:{port}")

    while True:
        client_sock, addr = server_socket.accept()
        print(f"[JSON][SYNC SERVER] Connection from {addr}")

        with client_sock:
            try:
                while True:
                    data_bytes = _recv_line(client_sock)
                    if not data_bytes:
                        break
                    data_str = data_bytes.decode('utf-8').strip()
                    data = json.loads(data_str)
                    handler_func(data, addr, client_sock)
            except (ConnectionResetError, json.JSONDecodeError) as e:
                print(f"[JSON][SYNC SERVER] Error: {e}")
            print(f"[JSON][SYNC SERVER] Connection closed from {addr}")

# -----------------------------
# Sync JSON Client
# -----------------------------

def send_json(host: str, port: int, data: dict, timeout: Optional[float] = None) -> Optional[dict]:
    """
    Sends a JSON message (sync) and waits for a JSON response.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))
        message = json.dumps(data) + '\n'
        sock.sendall(message.encode('utf-8'))

        try:
            response_bytes = _recv_line(sock)
            response_str = response_bytes.decode('utf-8').strip()
            return json.loads(response_str)
        except (socket.timeout, json.JSONDecodeError):
            return None

# -----------------------------
# Async JSON Server
# -----------------------------

async def start_json_server_async(
    port: int,
    handler_func: Callable[[dict, tuple, asyncio.StreamWriter], Awaitable[None]],
    host: str = '0.0.0.0'
):
    """
    Starts an async TCP server that communicates using JSON.
    """

    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        print(f"[JSON][ASYNC SERVER] Connection from {addr}")
        try:
            while True:
                data_bytes = await _recv_line_async(reader)
                if not data_bytes:
                    break
                data_str = data_bytes.decode('utf-8').strip()
                try:
                    data = json.loads(data_str)
                except json.JSONDecodeError:
                    print(f"[JSON][ASYNC SERVER] Invalid JSON from {addr}")
                    break
                await handler_func(data, addr, writer)
        except Exception as e:
            print(f"[JSON][ASYNC SERVER] Error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            print(f"[JSON][ASYNC SERVER] Connection closed from {addr}")

    server = await asyncio.start_server(handle_client, host, port)
    print(f"[JSON][ASYNC SERVER] Listening on {host}:{port}")
    async with server:
        await server.serve_forever()

# -----------------------------
# Async JSON Client
# -----------------------------

async def send_json_async(host: str, port: int, data: dict) -> Optional[dict]:
    """
    Sends a JSON message asynchronously and waits for JSON response.
    """
    reader, writer = await asyncio.open_connection(host, port)
    message = json.dumps(data) + '\n'
    writer.write(message.encode('utf-8'))
    await writer.drain()

    try:
        response_bytes = await _recv_line_async(reader)
        response_str = response_bytes.decode('utf-8').strip()
        response = json.loads(response_str)
    except json.JSONDecodeError:
        response = None

    writer.close()
    await writer.wait_closed()
    return response

# -----------------------------
# Sync Helper: send JSON response
# -----------------------------

def send_json_response(sock: socket.socket, data: dict):
    """Send JSON response (sync) ending with newline."""
    message = json.dumps(data) + '\n'
    sock.sendall(message.encode('utf-8'))

# -----------------------------
# Async Helper: send JSON response
# -----------------------------

async def send_json_response_async(writer: asyncio.StreamWriter, data: dict):
    """Send JSON response asynchronously ending with newline."""
    message = json.dumps(data) + '\n'
    writer.write(message.encode('utf-8'))
    await writer.drain()
