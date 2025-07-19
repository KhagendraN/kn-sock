from kn_sock import TCPConnectionPool

if __name__ == "__main__":
    # Replace with your actual certificate and key file paths
    CAFILE = None  # e.g., "ca.crt" for server verification
    CERTFILE = None  # e.g., "client.crt" for mutual TLS
    KEYFILE = None  # e.g., "client.key" for mutual TLS
    pool = TCPConnectionPool(
        "localhost",
        8443,
        max_size=3,
        idle_timeout=10,
        ssl=True,
        cafile=CAFILE,
        certfile=CERTFILE,
        keyfile=KEYFILE,
        verify=True,
    )
    with pool.connection() as conn:
        conn.sendall(b"Hello from SSL pool!")
        data = conn.recv(1024)
        print(f"[SSL POOL][CLIENT] Received: {data}")
    pool.closeall()
