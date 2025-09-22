from kn_sock import send_udp_multicast
import time

if __name__ == "__main__":
    GROUP = "224.0.0.1"
    PORT = 5007
    for i in range(3):
        send_udp_multicast(GROUP, PORT, f"Hello Multicast {i+1}")
        print(f"[MULTICAST][CLIENT] Sent message {i+1}")
        time.sleep(1)
