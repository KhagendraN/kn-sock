# examples/tcp_client.py

from easy_socket import send_tcp_message

if __name__ == "__main__":
    send_tcp_message("localhost", 8080, "Hello, TCP Server!")
