"""
Chat Application Example

Demonstrates a simple real-time chat using kn-sock's WebSocket server/client.

How to run:
    # Start the server
    python chat_app.py server

    # Start the client (in another terminal)
    python chat_app.py client
"""
import sys
from kn_sock import start_websocket_server, connect_websocket


def server():
    clients = []

    def handler(ws):
        clients.append(ws)
        print(f"[Server] Client connected: {ws.addr}")
        try:
            while ws.open:
                msg = ws.recv()
                if not msg:
                    break
                print(f"[Server] Received: {msg}")
                # Broadcast to all clients
                for c in clients:
                    if c.open:
                        c.send(f"{ws.addr}: {msg}")
        finally:
            ws.close()
            clients.remove(ws)
            print(f"[Server] Client disconnected: {ws.addr}")

    start_websocket_server("127.0.0.1", 9200, handler)


def client():
    ws = connect_websocket("127.0.0.1", 9200)
    print("[Client] Connected. Type messages and press Enter. Ctrl+C to exit.")
    import threading

    def recv_loop():
        while ws.open:
            msg = ws.recv()
            if msg:
                print("[Chat]", msg)

    threading.Thread(target=recv_loop, daemon=True).start()
    try:
        while True:
            msg = input()
            ws.send(msg)
    except KeyboardInterrupt:
        ws.close()
        print("[Client] Disconnected.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chat_app.py [server|client]")
        sys.exit(1)
    if sys.argv[1] == "server":
        server()
    else:
        client()
