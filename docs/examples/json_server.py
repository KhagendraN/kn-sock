# examples/json_server.py

import asyncio
from kn_sock import start_json_server_async, send_json_response_async


async def handle_client(data, addr, writer):
    print(f"Received JSON data from {addr}: {data}")
    await send_json_response_async(writer, {"status": "success"})


if __name__ == "__main__":
    asyncio.run(start_json_server_async(8082, handle_client))
