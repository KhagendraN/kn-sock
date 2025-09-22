# examples/udp_server.py

import threading
import time
from kn_sock import start_udp_server


def echo_handler(data, addr, sock):
    print(f"[UDP][SERVER] Received from {addr}: {data.decode()}")
    sock.sendto(b"Echo: " + data, addr)


if __name__ == "__main__":
    shutdown_event = threading.Event()
    server_thread = threading.Thread(
        target=start_udp_server,
        args=(8082, echo_handler),
        kwargs={"shutdown_event": shutdown_event},
        daemon=True,
    )
    server_thread.start()
    print("[UDP][SERVER] Running. Will shutdown in 10 seconds...")
    time.sleep(10)
    print("[UDP][SERVER] Triggering graceful shutdown...")
    shutdown_event.set()
    server_thread.join()
    print("[UDP][SERVER] Shutdown complete.")
