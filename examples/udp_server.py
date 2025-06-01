# examples/udp_server.py

import socket
from kn_sock import start_udp_server

def handle_client(data, addr, server_socket):
    print(f"Received data from {addr}: {data.decode('utf-8')}")
    server_socket.sendto(b"Message received", addr)

if __name__ == "__main__":
    start_udp_server(8081, handle_client)