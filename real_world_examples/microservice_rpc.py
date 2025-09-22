"""
Microservice RPC Example

Demonstrates remote procedure calls between services using kn-sock's RPC server/client.

How to run:
    # Start the server
    python microservice_rpc.py server

    # Start the client (in another terminal)
    python microservice_rpc.py client
"""
import sys
from kn_sock import start_rpc_server, RPCClient


def server():
    def add(a, b):
        return a + b

    def echo(msg):
        return f"Echo: {msg}"

    start_rpc_server(9300, functions={"add": add, "echo": echo})


def client():
    rpc = RPCClient("localhost", 9300)
    print("add(2, 3) =>", rpc.call("add", 2, 3))
    print("echo('hello') =>", rpc.call("echo", "hello"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python microservice_rpc.py [server|client]")
        sys.exit(1)
    if sys.argv[1] == "server":
        server()
    else:
        client()
