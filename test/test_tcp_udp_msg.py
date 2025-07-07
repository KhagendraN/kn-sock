import pytest
import asyncio
import threading
from kn_sock import (
    start_tcp_server, send_tcp_message,
    start_async_tcp_server, send_tcp_message_async,
    start_udp_server, send_udp_message,
    start_udp_server_async, send_udp_message_async,
)
from kn_sock.utils import get_free_port

# --- Sync TCP ---

@pytest.fixture
def run_sync_tcp_server():
    received_messages = []

    def handler(data, addr, client_socket):
        received_messages.append(data.decode())
        client_socket.sendall(b"Message received")

    port = get_free_port()
    server_thread = threading.Thread(target=start_tcp_server, args=(port, handler), daemon=True)
    server_thread.start()

    import time; time.sleep(1)
    yield received_messages, port

def test_sync_tcp(run_sync_tcp_server):
    import time
    received_messages, port = run_sync_tcp_server
    for _ in range(10):
        try:
            send_tcp_message("localhost", port, "Hello, Sync TCP!")
            break
        except ConnectionRefusedError:
            time.sleep(0.2)
    else:
        pytest.fail("TCP server did not start in time")
    time.sleep(0.5)
    assert "Hello, Sync TCP!" in received_messages, (
        "FAILURE: Sync TCP server did NOT receive the expected message."
    )
    print("SUCCESS: Sync TCP server received the expected message.")

# --- Async TCP ---

@pytest.mark.asyncio
async def test_async_tcp():
    received_messages = []

    async def handler(data, addr, writer):
        received_messages.append(data.decode())
        writer.write(b"Message received")
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    server_task = asyncio.create_task(start_async_tcp_server(9091, handler))
    await asyncio.sleep(1)  # wait for server to start

    await send_tcp_message_async("localhost", 9091, "Hello, Async TCP!")

    await asyncio.sleep(1)  # wait for message handling

    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

    assert "Hello, Async TCP!" in received_messages, (
        "FAILURE: Async TCP server did NOT receive the expected message."
    )
    print("SUCCESS: Async TCP server received the expected message.")

# --- Sync UDP ---

@pytest.fixture
def run_sync_udp_server():
    received_messages = []

    def handler(data, addr, server_socket):
        received_messages.append(data.decode())

    server_thread = threading.Thread(target=start_udp_server, args=(9092, handler), daemon=True)
    server_thread.start()

    import time; time.sleep(0.5)
    yield received_messages

def test_sync_udp(run_sync_udp_server):
    send_udp_message("localhost", 9092, "Hello, Sync UDP!")
    import time; time.sleep(0.5)
    assert "Hello, Sync UDP!" in run_sync_udp_server, (
        "FAILURE: Sync UDP server did NOT receive the expected message."
    )
    print("SUCCESS: Sync UDP server received the expected message.")

# --- Async UDP ---

@pytest.mark.asyncio
async def test_async_udp():
    port = get_free_port()
    received_messages = []

    async def handler(data, addr, transport):
        received_messages.append(data.decode())

    server_task = asyncio.create_task(start_udp_server_async(port, handler))
    await asyncio.sleep(2)

    await send_udp_message_async("localhost", port, "Hello, Async UDP!")

    await asyncio.sleep(2)

    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

    assert "Hello, Async UDP!" in received_messages, (
        "FAILURE: Async UDP server did NOT receive the expected message."
    )
    print("SUCCESS: Async UDP server received the expected message.")
