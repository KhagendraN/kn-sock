# examples/tcp_client.py

from kn_sock import send_tcp_message

if __name__ == "__main__":
    # Example: Connect to an IPv6 TCP server (localhost)
    send_tcp_message("::1", 8080, "Hello IPv6 Server!")
