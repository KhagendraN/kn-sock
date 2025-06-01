# examples/udp_client.py

from easy_socket import send_udp_message

if __name__ == "__main__":
    send_udp_message("localhost", 8081, "Hello, UDP Server!")
