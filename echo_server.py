# echo_server.py
# A simple echo server using kn_sock
# It listens on port 9001 and echoes back any data it receives
# Usage: python echo_server.py

from kn_sock import start_tcp_server

def echo(data, addr, conn):
    print(f"Connection from {addr}")
    try:
        print(f"Received: {data}")
        conn.sendall(b"Echo: " + data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        print(f"Closed connection to {addr}")

start_tcp_server(9001, echo, host="0.0.0.0")

