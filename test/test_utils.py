import os
import socket
import tempfile
from unittest import mock
import pytest

from kn_sock.utils import (
    get_free_port,
    get_local_ip,
    chunked_file_reader,
    recv_all,
    print_progress,
    is_valid_json
)

### get_free_port ###
def test_get_free_port_is_available():
    port = get_free_port()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", port))
            print(f"[SUCCESS] get_free_port returned available port: {port}")
    except Exception as e:
        print(f"[FAILED] get_free_port returned unavailable port {port}: {e}")
        raise

### get_local_ip ###
def test_get_local_ip_returns_ip():
    ip = get_local_ip()
    try:
        parts = ip.split(".")
        assert len(parts) == 4
        assert all(0 <= int(part) <= 255 for part in parts)
        print(f"[SUCCESS] get_local_ip returned a valid IP: {ip}")
    except Exception:
        print(f"[FAILED] get_local_ip returned an invalid IP: {ip}")
        raise

### chunked_file_reader ###
def test_chunked_file_reader_reads_in_chunks():
    content = b"abcdefghijklmnopqrstuvwxyz"
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        chunks = list(chunked_file_reader(tmp_path, chunk_size=5))
        assert b"".join(chunks) == content
        assert all(len(c) <= 5 for c in chunks)
        print(f"[SUCCESS] chunked_file_reader read all content in chunks.")
    except Exception as e:
        print(f"[FAILED] chunked_file_reader error: {e}")
        raise
    finally:
        os.remove(tmp_path)

### recv_all ###
def test_recv_all_receives_exact_bytes():
    server_sock, client_sock = socket.socketpair()
    test_data = b"hello world"
    client_sock.sendall(test_data)

    try:
        received = recv_all(server_sock, len(test_data))
        assert received == test_data
        print(f"[SUCCESS] recv_all received all data correctly.")
    except Exception as e:
        print(f"[FAILED] recv_all error: {e}")
        raise
    finally:
        server_sock.close()
        client_sock.close()

### print_progress ###
def test_print_progress_displays_correctly(capsys):
    try:
        print_progress(50, 100)
        captured = capsys.readouterr()
        assert "50.00%" in captured.out
        print(f"[SUCCESS] print_progress displayed correctly: {captured.out.strip()}")
    except Exception as e:
        print(f"[FAILED] print_progress error: {e}")
        raise

### is_valid_json ###
def test_is_valid_json_returns_true_for_valid():
    valid = '{"key": "value"}'
    try:
        assert is_valid_json(valid)
        print(f"[SUCCESS] is_valid_json correctly identified valid JSON.")
    except Exception as e:
        print(f"[FAILED] is_valid_json failed on valid JSON: {e}")
        raise

def test_is_valid_json_returns_false_for_invalid():
    invalid = "{invalid json}"
    try:
        assert not is_valid_json(invalid)
        print(f"[SUCCESS] is_valid_json correctly identified invalid JSON.")
    except Exception as e:
        print(f"[FAILED] is_valid_json failed on invalid JSON: {e}")
        raise
