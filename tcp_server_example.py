from kn_sock import start_tcp_server

def echo_handler(data, addr, conn):
    print(f"Received from {addr}: {data.decode()}")
    conn.sendall(b"Echo: " + data)

start_tcp_server(8080, echo_handler)

