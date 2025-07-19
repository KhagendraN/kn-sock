from kn_sock import TCPConnectionPool

if __name__ == "__main__":
    pool = TCPConnectionPool("localhost", 8080, max_size=3, idle_timeout=10)
    with pool.connection() as conn:
        conn.sendall(b"Hello from pool!")
        data = conn.recv(1024)
        print(f"[POOL][CLIENT] Received: {data}")
    pool.closeall()
