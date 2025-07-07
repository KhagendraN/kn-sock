# kn_sock/udp.py

import socket
import asyncio
from typing import Callable, Awaitable

BUFFER_SIZE = 1024

# -----------------------------
# 📥 Sync UDP Server
# -----------------------------

def start_udp_server(
    port: int,
    handler_func: Callable[[bytes, tuple, socket.socket], None],
    host: str = '0.0.0.0'
):
    """
    Starts a synchronous UDP server.
    Calls handler_func(data, addr, socket).
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"[UDP][SYNC] Server listening on {host}:{port}")

    while True:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        handler_func(data, addr, server_socket)

# -----------------------------
# 📤 Sync UDP Client
# -----------------------------

def send_udp_message(host: str, port: int, message: str):
    """
    Sends a message to a UDP server.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode('utf-8'), (host, port))
        print(f"[UDP][SYNC] Sent to {host}:{port}")

# -----------------------------
# 📥 Async UDP Server
# -----------------------------

async def start_udp_server_async(
    port: int,
    handler_func: Callable[[bytes, tuple, asyncio.DatagramTransport], Awaitable[None]],
    host: str = '0.0.0.0'
):
    """
    Starts an asynchronous UDP server using asyncio.
    Calls async handler_func(data, addr, transport).
    """

    class UDPProtocol(asyncio.DatagramProtocol):
        def __init__(self, loop):
            self.loop = loop

        def connection_made(self, transport):
            self.transport = transport
            print(f"[UDP][ASYNC] Server listening on {host}:{port}")

        def datagram_received(self, data, addr):
            asyncio.create_task(handler_func(data, addr, self.transport))

    loop = asyncio.get_running_loop()
    await loop.create_datagram_endpoint(
        lambda: UDPProtocol(loop),
        local_addr=(host, port)
    )

# -----------------------------
# 📤 Async UDP Client
# -----------------------------

async def send_udp_message_async(host: str, port: int, message: str):
    """
    Sends a message to a UDP server asynchronously.
    """
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: asyncio.DatagramProtocol(),
        remote_addr=(host, port)
    )
    transport.sendto(message.encode('utf-8'))
    print(f"[UDP][ASYNC] Sent to {host}:{port}")
    transport.close()
