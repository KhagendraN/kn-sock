# examples/tcp_server.py

import threading
import time
from kn_sock import start_tcp_server


def echo_handler(data, addr, client_socket):
    print(f"[SERVER] Received from {addr}: {data.decode()}")
    client_socket.sendall(b"Echo: " + data)


if __name__ == "__main__":
    # Example: Graceful shutdown for sync TCP server (IPv4 and IPv6 supported)
    # To run on IPv6 localhost, use host='::1'
    shutdown_event = threading.Event()
    server_thread = threading.Thread(
        target=start_tcp_server,
        args=(8080, echo_handler),
        kwargs={"host": "::1", "shutdown_event": shutdown_event},
        daemon=True,
    )
    server_thread.start()
    print("[SERVER] Running on IPv6 (::1). Will shutdown in 10 seconds...")
    time.sleep(10)
    print("[SERVER] Triggering graceful shutdown...")
    shutdown_event.set()
    server_thread.join()
    print("[SERVER] Shutdown complete.")
