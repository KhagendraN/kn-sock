# kn_sock/tcp.py

import socket
import threading
import asyncio
from typing import Callable, Awaitable

BUFFER_SIZE = 1024

# -----------------------------
# 🖥️ TCP Server (Synchronous)
# -----------------------------

def start_tcp_server(port: int, handler_func: Callable[[bytes, tuple, socket.socket], None], host: str = '0.0.0.0'):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[TCP] Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[TCP] Connection from {addr}")
        data = client_socket.recv(BUFFER_SIZE)
        if data:
            handler_func(data, addr, client_socket)
        client_socket.close()

# -----------------------------
# 🧵 Threaded TCP Server
# -----------------------------

def start_threaded_tcp_server(port: int, handler_func: Callable[[bytes, tuple, socket.socket], None], host: str = '0.0.0.0'):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print(f"[TCP] Threaded server listening on {host}:{port}")

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

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=client_thread, args=(client_socket, addr))
        thread.start()

# -----------------------------
# 📤 TCP Client (Sync)
# -----------------------------

def send_tcp_message(host: str, port: int, message: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
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
    host: str = '0.0.0.0'
):
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
        await server.serve_forever()

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
