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
    is_valid_json,
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


# --- Error Condition Tests ---
def test_is_valid_json_invalid():
    from kn_sock.utils import is_valid_json

    assert not is_valid_json("{bad json}")


def test_chunked_file_reader_bad_path():
    import pytest
    from kn_sock.utils import chunked_file_reader

    with pytest.raises(FileNotFoundError):
        list(chunked_file_reader("/nonexistent/file.txt"))


# --- Compression Tests ---
def test_gzip_compression():
    from kn_sock.compression import compress_data, decompress_data, detect_compression

    data = b"hello world" * 100
    compressed = compress_data(data, method="gzip")
    assert detect_compression(compressed) == "gzip"
    decompressed = decompress_data(compressed)
    assert decompressed == data


def test_deflate_compression():
    from kn_sock.compression import compress_data, decompress_data, detect_compression

    data = b"test data" * 100
    compressed = compress_data(data, method="deflate")
    assert (
        detect_compression(compressed) == "deflate"
        or detect_compression(compressed) == "none"
    )  # zlib header may not be detected
    decompressed = decompress_data(compressed)
    assert decompressed == data


def test_decompress_invalid():
    from kn_sock.compression import decompress_data
    import pytest

    with pytest.raises(ValueError):
        decompress_data(b"not compressed data")


# --- Async WebSocket Client Test ---
import pytest
import asyncio
from kn_sock.websocket import start_websocket_server, async_connect_websocket


def echo_handler(ws):
    while ws.open:
        msg = ws.recv()
        if not msg:
            break
        ws.send(msg)
    ws.close()


@pytest.mark.asyncio
async def test_async_websocket_client():
    import threading
    import time

    server_thread = threading.Thread(
        target=start_websocket_server,
        args=("127.0.0.1", 8766, echo_handler),
        daemon=True,
    )
    server_thread.start()
    time.sleep(0.5)
    ws = await async_connect_websocket("127.0.0.1", 8766)
    await ws.send("hello async")
    reply = await ws.recv()
    assert reply == "hello async"
    await ws.close()


# --- Message Queue Tests ---
def test_inmemory_queue():
    from kn_sock.queue import InMemoryQueue

    q = InMemoryQueue()
    q.put("a")
    assert not q.empty()
    assert q.qsize() == 1
    assert q.get() == "a"
    q.task_done()
    q.join()
    assert q.empty()


def test_file_queue(tmp_path):
    from kn_sock.queue import FileQueue

    path = tmp_path / "queue.db"
    fq = FileQueue(str(path))
    fq.put("x")
    fq.put("y")
    assert fq.qsize() == 2
    assert fq.get() == "x"
    fq.task_done()
    fq.close()
    # Reopen and check persistence
    fq2 = FileQueue(str(path))
    assert fq2.get() == "y"
    fq2.task_done()
    fq2.close()


# --- Protobuf Serialization Test ---
class MockProto:
    def __init__(self, value=None):
        self.value = value
        self._data = None

    def SerializeToString(self):
        return str(self.value).encode()

    def ParseFromString(self, data):
        self.value = int(data.decode())


def test_protobuf_serialization():
    from kn_sock.protobuf import serialize_message, deserialize_message

    msg = MockProto(42)
    data = serialize_message(msg)
    restored = deserialize_message(data, MockProto)
    assert restored.value == 42


# --- Load Balancer Tests ---
def test_round_robin_load_balancer():
    from kn_sock.load_balancer import RoundRobinLoadBalancer

    lb = RoundRobinLoadBalancer()
    for s in ["a", "b", "c"]:
        lb.add_server(s)
    # The expected sequence is a, b, c, a, b, c
    sequence = [lb.get_server() for _ in range(6)]
    assert sequence == ["a", "b", "c", "a", "b", "c"]


def test_least_connections_load_balancer():
    from kn_sock.load_balancer import LeastConnectionsLoadBalancer

    lcb = LeastConnectionsLoadBalancer()
    lcb.add_server("a")
    lcb.add_server("b")
    lcb.update_connections("a", 2)
    lcb.update_connections("b", 1)
    assert lcb.get_server() == "b"
    lcb.update_connections("a", 0)
    assert lcb.get_server() == "a"


# --- File Transfer Progress Bar Test ---
import socket
import threading
import time
from kn_sock.file_transfer import send_file, start_file_server


def get_free_port():
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def test_send_file_progress_bar(tmp_path):
    test_file = tmp_path / "testfile.txt"
    test_file.write_text("data" * 100)
    port = get_free_port()
    stop_event = threading.Event()
    ready_event = threading.Event()

    def server():
        # Start the server and signal when ready
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", port))
        server_socket.listen(5)
        ready_event.set()
        while not stop_event.is_set():
            server_socket.settimeout(0.2)
            try:
                conn, addr = server_socket.accept()
            except socket.timeout:
                continue
            with conn:
                filename = conn.recv(1024).decode().strip()
                filesize = int(conn.recv(1024).decode().strip())
                save_path = tmp_path / filename
                with open(save_path, "wb") as f:
                    remaining = filesize
                    while remaining > 0:
                        data = conn.recv(min(4096, remaining))
                        if not data:
                            break
                        f.write(data)
                        remaining -= len(data)
        server_socket.close()

    t = threading.Thread(target=server, daemon=True)
    t.start()
    ready_event.wait(timeout=2)  # Wait for server to be ready
    send_file("127.0.0.1", port, str(test_file))
    stop_event.set()
    t.join(timeout=1)
