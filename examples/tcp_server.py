# examples/tcp_server.py

import socket
from easy_socket import start_tcp_server

def handle_client(data, addr, client_socket):
    print(f"Received data from {addr}: {data.decode('utf-8')}")
    client_socket.sendall(b"Message received")

if __name__ == "__main__":
    start_tcp_server(8080, handle_client)
