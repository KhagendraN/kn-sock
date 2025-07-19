from kn_sock import start_ssl_tcp_server
import threading
import time


def echo_handler(data, addr, client_socket):
    print(f"[SSL][SERVER] Received from {addr}: {data.decode()}")
    client_socket.sendall(b"Echo: " + data)


if __name__ == "__main__":
    # Replace with your actual certificate and key file paths
    CERTFILE = "server.crt"
    KEYFILE = "server.key"
    CAFILE = None  # e.g., "ca.crt" for client cert verification
    shutdown_event = threading.Event()
    server_thread = threading.Thread(
        target=start_ssl_tcp_server,
        args=(8443, echo_handler, CERTFILE, KEYFILE),
        kwargs={
            "cafile": CAFILE,
            "require_client_cert": False,
            "shutdown_event": shutdown_event,
        },
        daemon=True,
    )
    server_thread.start()
    print("[SSL][SERVER] Running. Will shutdown in 10 seconds...")
    time.sleep(10)
    print("[SSL][SERVER] Triggering graceful shutdown...")
    shutdown_event.set()
    server_thread.join()
    print("[SSL][SERVER] Shutdown complete.")
