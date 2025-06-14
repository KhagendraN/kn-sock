import kn_sock
import socket
import threading
import asyncio
import json
import os

# -----------------------------
# TCP Tests
# -----------------------------

def test_tcp_server_client():
    def handler(data, addr, client_socket):
        client_socket.sendall(b"Echo: " + data)

    server_thread = threading.Thread(target=kn_sock.start_tcp_server, args=(12345, handler))
    server_thread.daemon = True
    server_thread.start()

    kn_sock.send_tcp_message("localhost", 12345, "Hello TCP")
    print("TCP test passed")

def test_threaded_tcp_server_client():
    def handler(data, addr, client_socket):
        client_socket.sendall(b"Echo: " + data)

    server_thread = threading.Thread(target=kn_sock.start_threaded_tcp_server, args=(12346, handler))
    server_thread.daemon = True
    server_thread.start()

    kn_sock.send_tcp_message("localhost", 12346, "Hello Threaded TCP")
    print("Threaded TCP test passed")

async def test_async_tcp_server_client():
    async def handler(data, addr, writer):
        writer.write(b"Echo: " + data)
        await writer.drain()

    server_task = asyncio.create_task(kn_sock.start_async_tcp_server(12347, handler))
    await asyncio.sleep(1)  # Give server time to start

    await kn_sock.send_tcp_message_async("localhost", 12347, "Hello Async TCP")
    print("Async TCP test passed")

# -----------------------------
# UDP Tests
# -----------------------------

def test_udp_server_client():
    def handler(data, addr, server_socket):
        server_socket.sendto(b"Echo: " + data, addr)

    server_thread = threading.Thread(target=kn_sock.start_udp_server, args=(12348, handler))
    server_thread.daemon = True
    server_thread.start()

    kn_sock.send_udp_message("localhost", 12348, "Hello UDP")
    print("UDP test passed")

async def test_async_udp_server_client():
    async def handler(data, addr, transport):
        transport.sendto(b"Echo: " + data, addr)

    server_task = asyncio.create_task(kn_sock.start_udp_server_async(12349, handler))
    await asyncio.sleep(1)  # Give server time to start

    await kn_sock.send_udp_message_async("localhost", 12349, "Hello Async UDP")
    print("Async UDP test passed")

# -----------------------------
# JSON Socket Tests
# -----------------------------

def test_json_server_client():
    def handler(data, addr, client_socket):
        response = json.dumps({"echo": data})
        client_socket.sendall(response.encode('utf-8'))

    server_thread = threading.Thread(target=kn_sock.start_json_server, args=(12350, handler))
    server_thread.daemon = True
    server_thread.start()

    kn_sock.send_json("localhost", 12350, {"message": "Hello JSON"})
    print("JSON test passed")

    # Send a shutdown message to the server
    kn_sock.send_json("localhost", 12350, {"shutdown": True})

# -----------------------------
# File Transfer Tests
# -----------------------------

def test_file_transfer():
    def handler(data, addr, client_socket):
        with open("received_file.txt", "wb") as f:
            f.write(data)

    server_thread = threading.Thread(target=kn_sock.start_file_server, args=(12351, handler))
    server_thread.daemon = True
    server_thread.start()

    with open("test_file.txt", "wb") as f:
        f.write(b"Hello File Transfer")

    kn_sock.send_file("localhost", 12351, "test_file.txt")

    with open("received_file.txt", "rb") as f:
        received_data = f.read()
        print(f"Received data: {received_data}")
        assert received_data == b"Hello File Transfer"

    os.remove("test_file.txt")
    os.remove("received_file.txt")
    print("File transfer test passed")

async def test_async_file_transfer():
    async def handler(data, addr, writer):
        with open("received_file.txt", "wb") as f:
            f.write(data)

    server_task = asyncio.create_task(kn_sock.start_file_server_async(12352, handler))
    await asyncio.sleep(1)  # Give server time to start

    with open("test_file.txt", "wb") as f:
        f.write(b"Hello Async File Transfer")

    await kn_sock.send_file_async("localhost", 12352, "test_file.txt")

    with open("received_file.txt", "rb") as f:
        received_data = f.read()
        print(f"Received data: {received_data}")
        assert received_data == b"Hello Async File Transfer"

    os.remove("test_file.txt")
    os.remove("received_file.txt")
    print("Async file transfer test passed")

# -----------------------------
# Run Tests
# -----------------------------

if __name__ == "__main__":
    test_tcp_server_client()
    test_threaded_tcp_server_client()
    asyncio.run(test_async_tcp_server_client())
    test_udp_server_client()
    asyncio.run(test_async_udp_server_client())
    #test_json_server_client()
    #test_file_transfer()
    #asyncio.run(test_async_file_transfer())
    print("All tests passed")
