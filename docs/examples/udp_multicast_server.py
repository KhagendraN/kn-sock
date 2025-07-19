import threading
import time
from kn_sock import start_udp_multicast_server


def handler(data, addr, sock):
    print(f"[MULTICAST][SERVER] Received from {addr}: {data.decode()}")


if __name__ == "__main__":
    GROUP = "224.0.0.1"
    PORT = 5007
    shutdown_event = threading.Event()
    server_thread = threading.Thread(
        target=start_udp_multicast_server,
        args=(GROUP, PORT, handler),
        kwargs={"shutdown_event": shutdown_event},
        daemon=True,
    )
    server_thread.start()
    print("[MULTICAST][SERVER] Running. Will shutdown in 10 seconds...")
    time.sleep(10)
    print("[MULTICAST][SERVER] Triggering graceful shutdown...")
    shutdown_event.set()
    server_thread.join()
    print("[MULTICAST][SERVER] Shutdown complete.")
