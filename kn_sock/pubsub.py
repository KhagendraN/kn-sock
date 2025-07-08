import socket
import threading
import json
from typing import Callable, Dict, Set, Optional

class PubSubServer:
    def __init__(self):
        self.topics: Dict[str, Set[socket.socket]] = {}
        self.lock = threading.Lock()

    def subscribe(self, topic: str, client_sock: socket.socket):
        with self.lock:
            self.topics.setdefault(topic, set()).add(client_sock)

    def unsubscribe(self, topic: str, client_sock: socket.socket):
        with self.lock:
            if topic in self.topics:
                self.topics[topic].discard(client_sock)
                if not self.topics[topic]:
                    del self.topics[topic]

    def publish(self, topic: str, message: str):
        with self.lock:
            for sock in list(self.topics.get(topic, [])):
                try:
                    data = json.dumps({"topic": topic, "message": message}).encode() + b"\n"
                    sock.sendall(data)
                except Exception:
                    self.topics[topic].discard(sock)

    def remove_client(self, client_sock: socket.socket):
        with self.lock:
            for topic in list(self.topics):
                self.topics[topic].discard(client_sock)
                if not self.topics[topic]:
                    del self.topics[topic]

def start_pubsub_server(
    port: int,
    handler_func: Optional[Callable[[dict, socket.socket, PubSubServer], None]] = None,
    host: str = '0.0.0.0',
    shutdown_event: Optional[threading.Event] = None
):
    """
    Start a TCP pub/sub server. Handles subscribe, unsubscribe, and publish actions.
    Args:
        port (int): Port to bind.
        handler_func (callable, optional): Custom handler for messages (default: built-in).
        host (str): Host to bind (default '0.0.0.0').
        shutdown_event (threading.Event, optional): For graceful shutdown.
    """
    server = PubSubServer()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print(f"[PubSub][SERVER] Listening on {host}:{port}")
    def client_thread(client_sock, addr):
        try:
            buffer = b''
            while True:
                chunk = client_sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    try:
                        msg = json.loads(line.decode())
                    except Exception:
                        continue
                    if handler_func:
                        handler_func(msg, client_sock, server)
                    else:
                        action = msg.get('action')
                        topic = msg.get('topic')
                        if action == 'subscribe':
                            server.subscribe(topic, client_sock)
                        elif action == 'unsubscribe':
                            server.unsubscribe(topic, client_sock)
                        elif action == 'publish':
                            server.publish(topic, msg.get('message', ''))
        finally:
            server.remove_client(client_sock)
            client_sock.close()
    try:
        while True:
            if shutdown_event is not None and shutdown_event.is_set():
                print("[PubSub][SERVER] Shutdown event set. Stopping server.")
                break
            sock.settimeout(1.0)
            try:
                client_sock, addr = sock.accept()
            except socket.timeout:
                continue
            threading.Thread(target=client_thread, args=(client_sock, addr), daemon=True).start()
    finally:
        sock.close()
        print("[PubSub][SERVER] Shutdown complete.")

class PubSubClient:
    """
    Simple TCP pub/sub client. Use subscribe, unsubscribe, publish, and recv methods.
    """
    def __init__(self, host: str, port: int):
        self.sock = socket.create_connection((host, port))
        self.lock = threading.Lock()
        self.recv_buffer = b''

    def subscribe(self, topic: str):
        self._send({"action": "subscribe", "topic": topic})

    def unsubscribe(self, topic: str):
        self._send({"action": "unsubscribe", "topic": topic})

    def publish(self, topic: str, message: str):
        self._send({"action": "publish", "topic": topic, "message": message})

    def recv(self, timeout: float = None) -> Optional[dict]:
        self.sock.settimeout(timeout)
        while True:
            if b'\n' in self.recv_buffer:
                line, self.recv_buffer = self.recv_buffer.split(b'\n', 1)
                try:
                    return json.loads(line.decode())
                except Exception:
                    continue
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    return None
                self.recv_buffer += chunk
            except socket.timeout:
                return None

    def _send(self, msg: dict):
        with self.lock:
            self.sock.sendall(json.dumps(msg).encode() + b'\n')

    def close(self):
        self.sock.close() 