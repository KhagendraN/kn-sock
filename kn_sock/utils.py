# kn_sock/utils.py

import os
import socket
import json
from typing import Generator, Optional

# -----------------------------
# 🌐 Network Utilities
# -----------------------------

def get_free_port() -> int:
    """Find a free port for TCP binding (useful for tests)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def get_local_ip() -> str:
    """Returns the local IP address of the current machine."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # This doesn't actually connect, it's just to get the right interface
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

# -----------------------------
# 📁 File Utilities
# -----------------------------

def chunked_file_reader(filepath: str, chunk_size: int = 4096) -> Generator[bytes, None, None]:
    """Yields file data in chunks for streaming transfer."""
    with open(filepath, 'rb') as f:
        while (chunk := f.read(chunk_size)):
            yield chunk

def recv_all(sock: socket.socket, total_bytes: int) -> bytes:
    """Receives exactly `total_bytes` from a socket."""
    data = b''
    while len(data) < total_bytes:
        chunk = sock.recv(total_bytes - len(data))
        if not chunk:
            break
        data += chunk
    return data

# -----------------------------
# 📊 Progress Display
# -----------------------------

def print_progress(received: int, total: int):
    """Prints file transfer progress in percentage."""
    percent = (received / total) * 100
    print(f"\rProgress: {percent:.2f}% ({received}/{total} bytes)", end='')

# -----------------------------
# 🧪 JSON Utility
# -----------------------------

def is_valid_json(data: str) -> bool:
    """Checks whether a string is valid JSON."""
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False
