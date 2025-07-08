import socket
import threading
import json
from typing import Callable, Dict, Any, Optional

class RPCServer:
    def __init__(self):
        self.functions: Dict[str, Callable] = {}
        self.lock = threading.Lock()

    def register(self, name: str, func: Callable):
        with self.lock:
            self.functions[name] = func

    def handle(self, request: dict) -> dict:
        method = request.get('method')
        params = request.get('params', [])
        kwargs = request.get('kwargs', {})
        if method not in self.functions:
            return {"error": f"Method '{method}' not found"}
        try:
            result = self.functions[method](*params, **kwargs)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

def start_rpc_server(
    port: int,
    register_funcs: Dict[str, Callable],
    host: str = '0.0.0.0',
    shutdown_event: Optional[threading.Event] = None
):
    """
    Start a TCP JSON-RPC server. Registers functions and handles remote calls.
    Args:
        port (int): Port to bind.
        register_funcs (dict): Mapping of function names to callables.
        host (str): Host to bind (default '0.0.0.0').
        shutdown_event (threading.Event, optional): For graceful shutdown.
    """
    server = RPCServer()
    for name, func in register_funcs.items():
        server.register(name, func)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print(f"[RPC][SERVER] Listening on {host}:{port}")
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
                        req = json.loads(line.decode())
                    except Exception:
                        continue
                    resp = server.handle(req)
                    client_sock.sendall(json.dumps(resp).encode() + b'\n')
        finally:
            client_sock.close()
    try:
        while True:
            if shutdown_event is not None and shutdown_event.is_set():
                print("[RPC][SERVER] Shutdown event set. Stopping server.")
                break
            sock.settimeout(1.0)
            try:
                client_sock, addr = sock.accept()
            except socket.timeout:
                continue
            threading.Thread(target=client_thread, args=(client_sock, addr), daemon=True).start()
    finally:
        sock.close()
        print("[RPC][SERVER] Shutdown complete.")

class RPCClient:
    """
    Simple TCP JSON-RPC client. Use call(method, *args, **kwargs) to invoke remote functions.
    """
    def __init__(self, host: str, port: int):
        self.sock = socket.create_connection((host, port))
        self.lock = threading.Lock()
        self.recv_buffer = b''

    def call(self, method: str, *args, **kwargs) -> Any:
        req = {"method": method, "params": args, "kwargs": kwargs}
        with self.lock:
            self.sock.sendall(json.dumps(req).encode() + b'\n')
            while True:
                if b'\n' in self.recv_buffer:
                    line, self.recv_buffer = self.recv_buffer.split(b'\n', 1)
                    try:
                        resp = json.loads(line.decode())
                    except Exception:
                        continue
                    if 'result' in resp:
                        return resp['result']
                    elif 'error' in resp:
                        raise Exception(resp['error'])
                chunk = self.sock.recv(4096)
                if not chunk:
                    raise ConnectionError("Connection closed")
                self.recv_buffer += chunk

    def close(self):
        self.sock.close() 