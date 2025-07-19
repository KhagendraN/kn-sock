from kn_sock import PubSubClient
import time

if __name__ == "__main__":
    client = PubSubClient("127.0.0.1", 9000)
    client.subscribe("news")
    print("[PubSub][CLIENT] Subscribed to 'news'")
    client.publish("news", "Hello, subscribers!")
    print("[PubSub][CLIENT] Published to 'news'")
    msg = client.recv(timeout=2)
    print(f"[PubSub][CLIENT] Received: {msg}")
    client.close()
