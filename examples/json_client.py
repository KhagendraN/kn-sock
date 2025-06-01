# examples/json_client.py

import asyncio
from easy_socket import send_json_async

async def main():
    response = await send_json_async("localhost", 8082, {"message": "Hello, JSON Server!"})
    print(f"Server response: {response}")

if __name__ == "__main__":
    asyncio.run(main())