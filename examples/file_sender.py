# examples/file_sender.py

from kn_sock import send_file

if __name__ == "__main__":
    send_file("localhost", 8080, "Assets/test.txt")
    send_file("localhost", 8080, "Assets/test2.json")
    send_file("localhost", 8080, "Assets/Sahanavhabatu.mp3")
    # after execution files should be available on Assets/server/ directory

# --- Example: File send with progress bar ---
# from kn_sock import send_file
# send_file('localhost', 8080, 'file.txt', show_progress=True)
