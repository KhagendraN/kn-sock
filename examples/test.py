import asyncio
from kn_sock import start_async_tcp_server


async def handle_tcp_message(data, addr, writer):
    """
    Handle incoming TCP messages asynchronously.

    Args:
        data (bytes): The data received from the client.
        addr (tuple): The address of the client.
        writer (asyncio.StreamWriter): The writer object for the client.
    """
    print(f"Received from {addr}: {data.decode('utf-8')}")
    writer.write(b"Message received")
    await writer.drain()


asyncio.run(start_async_tcp_server(8080, handle_tcp_message))
