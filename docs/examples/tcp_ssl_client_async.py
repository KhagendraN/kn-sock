import asyncio
from kn_sock import send_ssl_tcp_message_async


async def main():
    HOST = "localhost"
    PORT = 8443
    MESSAGE = "Hello Secure Server!"
    CAFILE = None  # e.g., "ca.crt" for server verification
    CERTFILE = None  # e.g., "client.crt" for mutual TLS
    KEYFILE = None  # e.g., "client.key" for mutual TLS
    await send_ssl_tcp_message_async(
        HOST,
        PORT,
        MESSAGE,
        cafile=CAFILE,
        certfile=CERTFILE,
        keyfile=KEYFILE,
        verify=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
