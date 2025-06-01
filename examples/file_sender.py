# examples/file_sender.py

from easy_socket import send_file

if __name__ == "__main__":
    send_file("localhost", 8083, "/home/khagendra/programs/PyPI_projects/shocketProject/exp.txt")