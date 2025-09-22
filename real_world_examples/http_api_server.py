"""
HTTP API Server Example

Demonstrates serving static files and a simple API using kn-sock's HTTP server.

How to run:
    # Start the server (serves current directory)
    python http_api_server.py

Then visit http://localhost:9500/ in your browser.
"""
import os
from kn_sock import start_http_server


def hello_route(request, client_sock):
    return (200, "text/plain", b"Hello from kn-sock API!")


def main():
    static_dir = os.getcwd()
    routes = {"/api/hello": hello_route}
    print(f"[HTTPServer] Serving static files from: {static_dir}")
    start_http_server(9500, static_dir=static_dir, routes=routes)


if __name__ == "__main__":
    main()
