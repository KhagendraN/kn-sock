"""
File Transfer Example

Demonstrates secure file transfer between two machines using kn-sock's file server/client.

How to run:
    # Start the server (in the directory to save files)
    python file_transfer.py server

    # Start the client (in another terminal, specify file to send)
    python file_transfer.py client <file_to_send>
"""
import sys
import os
from kn_sock import start_file_server, send_file


def server():
    save_dir = os.getcwd()
    print(f"[FileServer] Saving files to: {save_dir}")
    start_file_server(9100, save_dir)


def client():
    if len(sys.argv) < 3:
        print("Usage: python file_transfer.py client <file_to_send>")
        sys.exit(1)
    file_path = sys.argv[2]
    send_file("localhost", 9100, file_path)
    print(f"[FileClient] Sent file: {file_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python file_transfer.py [server|client <file_to_send>]")
        sys.exit(1)
    if sys.argv[1] == "server":
        server()
    else:
        client()
