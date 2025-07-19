import asyncio
from kn_sock import start_async_ssl_tcp_server


async def echo_handler(data, addr, writer):
    print(f"[SSL][ASYNC][SERVER] Received from {addr}: {data.decode()}")
    writer.write(b"Echo: " + data)
    await writer.drain()


async def main():
    # Replace with your actual certificate and key file paths
    CERTFILE = "server.crt"
    KEYFILE = "server.key"
    CAFILE = None  # e.g., "ca.crt" for client cert verification
    shutdown_event = asyncio.Event()
    server_task = asyncio.create_task(
        start_async_ssl_tcp_server(
            8443,
            echo_handler,
            certfile=CERTFILE,
            keyfile=KEYFILE,
            cafile=CAFILE,
            require_client_cert=False,
            shutdown_event=shutdown_event,
        )
    )
    print("[SSL][ASYNC][SERVER] Running. Will shutdown in 10 seconds...")
    await asyncio.sleep(10)
    print("[SSL][ASYNC][SERVER] Triggering graceful shutdown...")
    shutdown_event.set()
    await server_task
    print("[SSL][ASYNC][SERVER] Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
