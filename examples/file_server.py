# examples/file_server.py

from kn_sock import start_file_server

if __name__ == "__main__":
    start_file_server(8080, "Assets/server")
