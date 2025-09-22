"""
Remote Control Example

Demonstrates remote monitoring and control of an application using kn-sock's JSON server/client.

How to run:
    # Start the server
    python remote_control.py server

    # Start the client (in another terminal)
    python remote_control.py client <command>
"""
import sys
from kn_sock import start_json_server, send_json


def server():
    def handler(data, addr, conn):
        print(f"[Server] Received: {data}")
        cmd = data.get("command")
        if cmd == "status":
            return {"status": "running"}
        elif cmd == "restart":
            return {"result": "restarting..."}
        else:
            return {"error": "unknown command"}

    start_json_server(9400, handler)


def client():
    if len(sys.argv) < 3:
        print("Usage: python remote_control.py client <command>")
        sys.exit(1)
    cmd = sys.argv[2]
    response = send_json("localhost", 9400, {"command": cmd})
    print("Server response:", response)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remote_control.py [server|client <command>]")
        sys.exit(1)
    if sys.argv[1] == "server":
        server()
    else:
        client()
