# examples/udp_client.py

from kn_sock import send_udp_message

if __name__ == "__main__":
    send_udp_message("localhost", 8081, "Hello, UDP Server!")
