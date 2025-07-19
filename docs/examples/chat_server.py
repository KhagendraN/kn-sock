from kn_sock import start_tcp_server


def handle_tcp_message(data, addr, client_socket):
    """
    Handle incoming TCP messages.

    Args:
        data (bytes): The data received from the client.
        addr (tuple): The address of the client.
        client_socket (socket.socket): The client socket.
    """
    print(f"Received from {addr}: {data.decode('utf-8')}")
    client_socket.sendall(b"Message received")


start_tcp_server(8080, handle_tcp_message)
