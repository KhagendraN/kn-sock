import threading
import time
from kn_sock import start_rpc_server


def add(a, b):
    return a + b


def echo(msg):
    return msg


if __name__ == "__main__":
    funcs = {"add": add, "echo": echo}
    shutdown_event = threading.Event()
    server_thread = threading.Thread(
        target=start_rpc_server,
        args=(9001, funcs),
        kwargs={"shutdown_event": shutdown_event},
        daemon=True,
    )
    server_thread.start()
    print("[RPC][SERVER] Running. Will shutdown in 10 seconds...")
    time.sleep(10)
    print("[RPC][SERVER] Triggering graceful shutdown...")
    shutdown_event.set()
    server_thread.join()
    print("[RPC][SERVER] Shutdown complete.")
