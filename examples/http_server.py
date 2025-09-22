import threading
import time
import os
from kn_sock import start_http_server


def hello_route(request, client_sock):
    client_sock.sendall(
        b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nHello"
    )


def echo_post(request, client_sock):
    # Echo back the POST body
    body = request["raw"].split(b"\r\n\r\n", 1)[-1]
    resp = (
        b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: "
        + str(len(body)).encode()
        + b"\r\n\r\n"
        + body
    )
    client_sock.sendall(resp)


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    with open("static/index.html", "w") as f:
        f.write("<h1>Hello from static file!</h1>")
    routes = {
        ("GET", "/hello"): hello_route,
        ("POST", "/echo"): echo_post,
    }
    shutdown_event = threading.Event()
    server_thread = threading.Thread(
        target=start_http_server,
        args=("127.0.0.1", 8080),
        kwargs={
            "static_dir": "static",
            "routes": routes,
            "shutdown_event": shutdown_event,
        },
        daemon=True,
    )
    server_thread.start()
    print("[HTTP][SERVER] Running. Will shutdown in 10 seconds...")
    time.sleep(10)
    print("[HTTP][SERVER] Triggering graceful shutdown...")
    shutdown_event.set()
    server_thread.join()
    print("[HTTP][SERVER] Shutdown complete.")
