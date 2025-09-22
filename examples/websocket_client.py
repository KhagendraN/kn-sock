from kn_sock import connect_websocket
import time

if __name__ == "__main__":
    ws = connect_websocket("127.0.0.1", 8765)
    print("[WebSocket][CLIENT] Connected to server.")
    ws.send("Hello WebSocket!")
    print(f"[WebSocket][CLIENT] Sent: Hello WebSocket!")
    reply = ws.recv()
    print(f"[WebSocket][CLIENT] Received: {reply}")
    ws.close()
    print("[WebSocket][CLIENT] Connection closed.")
