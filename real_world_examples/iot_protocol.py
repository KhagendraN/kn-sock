"""
IoT Protocol Example

Demonstrates a custom communication protocol for IoT devices using kn-sock's JSON server/client.

How to run:
    # Start the server
    python iot_protocol.py server

    # Start the client (in another terminal)
    python iot_protocol.py client
"""
import sys
from kn_sock import start_json_server, send_json


def server():
    def handler(data, addr, conn):
        print(f"Received from {addr}: {data}")
        # Respond with a command
        return {"command": "fan_on"}

    start_json_server(9000, handler)


def client():
    data = {"sensor_id": "temp_01", "temperature": 25.5}
    response = send_json("localhost", 9000, data)
    print("Server response:", response)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python iot_protocol.py [server|client]")
        sys.exit(1)
    if sys.argv[1] == "server":
        server()
    else:
        client()
