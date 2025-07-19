from kn_sock import RPCClient

if __name__ == "__main__":
    client = RPCClient("127.0.0.1", 9001)
    result = client.call("add", 2, 3)
    print(f"[RPC][CLIENT] add(2, 3) = {result}")
    result = client.call("echo", msg="Hello RPC!")
    print(f"[RPC][CLIENT] echo(msg='Hello RPC!') = {result}")
    client.close()
