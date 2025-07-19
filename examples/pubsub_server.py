import threading
import time
from kn_sock import start_pubsub_server

if __name__ == "__main__":
    shutdown_event = threading.Event()
    server_thread = threading.Thread(
        target=start_pubsub_server,
        args=(9000,),
        kwargs={"shutdown_event": shutdown_event},
        daemon=True,
    )
    server_thread.start()
    print("[PubSub][SERVER] Running. Will shutdown in 10 seconds...")
    time.sleep(10)
    print("[PubSub][SERVER] Triggering graceful shutdown...")
    shutdown_event.set()
    server_thread.join()
    print("[PubSub][SERVER] Shutdown complete.")
