# examples/json_client.py

import asyncio
from kn_sock import send_json_async


async def main():
    response = await send_json_async(
        "localhost", 8082, {"message": "Hello, JSON Server!"}
    )
    print(f"Server response: {response}")


if __name__ == "__main__":
    asyncio.run(main())

# --- Example: Sending compressed JSON ---
# import socket
# from kn_sock.compression import compress_data
# import json
# data = json.dumps({"msg": "hello", "big": "x"*1000}).encode()
# compressed = compress_data(data, method='gzip')
# s = socket.socket()
# s.connect(("localhost", 8080))
# s.sendall(compressed)
# s.close()

# --- Example: Using kn_sock Queues ---
# from kn_sock.queue import InMemoryQueue, FileQueue
# q = InMemoryQueue()
# q.put('msg1')
# print(q.get())
#
# fq = FileQueue('queue.db')
# fq.put('msg2')
# print(fq.get())
# fq.close()

# --- Example: Using kn_sock Protobuf ---
# from kn_sock.protobuf import serialize_message, deserialize_message
# from my_proto_pb2 import MyMessage
# msg = MyMessage(field1='abc', field2=123)
# data = serialize_message(msg)
# restored = deserialize_message(data, MyMessage)
# print(restored)

# --- Example: Using kn_sock Load Balancers ---
# from kn_sock.load_balancer import RoundRobinLoadBalancer, LeastConnectionsLoadBalancer
# lb = RoundRobinLoadBalancer()
# lb.add_server('a')
# lb.add_server('b')
# print(lb.get_server())
# print(lb.get_server())
#
# lcb = LeastConnectionsLoadBalancer()
# lcb.add_server('a')
# lcb.add_server('b')
# lcb.update_connections('a', 2)
# lcb.update_connections('b', 1)
# print(lcb.get_server())
