import asyncio
from kn_sock import start_udp_server_async


async def echo_handler(data, addr, transport):
    print(f"[UDP][ASYNC][SERVER] Received from {addr}: {data.decode()}")
    transport.sendto(b"Echo: " + data, addr)


async def main():
    shutdown_event = asyncio.Event()
    server_task = asyncio.create_task(
        start_udp_server_async(8083, echo_handler, shutdown_event=shutdown_event)
    )
    print("[UDP][ASYNC][SERVER] Running. Will shutdown in 10 seconds...")
    await asyncio.sleep(10)
    print("[UDP][ASYNC][SERVER] Triggering graceful shutdown...")
    shutdown_event.set()
    await server_task
    print("[UDP][ASYNC][SERVER] Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
