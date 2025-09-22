import asyncio
from kn_sock import send_tcp_message_async

while True:
    msg = input("Your message : ")
    asyncio.run(send_tcp_message_async("localhost", 8080, msg))
