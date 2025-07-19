import threading
import time
from kn_sock import start_websocket_server


def echo_handler(ws):
    print(f"[WebSocket][SERVER] Client connected: {ws.addr}")
    try:
        while ws.open:
            msg = ws.recv()
            if not msg:
                break
            print(f"[WebSocket][SERVER] Received: {msg}")
            ws.send(f"Echo: {msg}")
    finally:
        ws.close()
        print(f"[WebSocket][SERVER] Client disconnected: {ws.addr}")


if __name__ == "__main__":
    shutdown_event = threading.Event()
    server_thread = threading.Thread(
        target=start_websocket_server,
        args=("127.0.0.1", 8765, echo_handler),
        kwargs={"shutdown_event": shutdown_event},
        daemon=True,
    )
    server_thread.start()
    print("[WebSocket][SERVER] Running. Will shutdown in 10 seconds...")
    time.sleep(10)
    print("[WebSocket][SERVER] Triggering graceful shutdown...")
    shutdown_event.set()
    server_thread.join()
    print("[WebSocket][SERVER] Shutdown complete.")
