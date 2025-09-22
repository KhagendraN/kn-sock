from kn_sock import send_ssl_tcp_message

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8443
    MESSAGE = "Hello Secure Server!"
    CAFILE = None  # e.g., "ca.crt" for server verification
    CERTFILE = None  # e.g., "client.crt" for mutual TLS
    KEYFILE = None  # e.g., "client.key" for mutual TLS
    send_ssl_tcp_message(
        HOST,
        PORT,
        MESSAGE,
        cafile=CAFILE,
        certfile=CERTFILE,
        keyfile=KEYFILE,
        verify=True,
    )
