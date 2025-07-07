import threading
import time
import socket
import json
import pytest
from kn_sock import send_json

# This is a helper to run a *single-connection* JSON server for testing
def run_single_connection_json_server(port, handler, stop_event):
    """
    Starts a server that accepts only one connection, processes one message,
    then stops (for clean pytest testing).
    """
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_sock.bind(('0.0.0.0', port))
    srv_sock.listen(1)
    srv_sock.settimeout(1)  # 1 second timeout to periodically check stop_event

    try:
        while not stop_event.is_set():
            try:
                client_sock, addr = srv_sock.accept()
            except socket.timeout:
                continue
            with client_sock:
                # Receive data - assuming JSON terminated by newline or fixed protocol
                data = client_sock.recv(4096)
                if not data:
                    continue
                try:
                    decoded = json.loads(data.decode())
                except Exception:
                    # Invalid JSON - ignore or break
                    break
                handler(decoded, addr, client_sock)
                # After handling one message, stop server
                stop_event.set()
    finally:
        srv_sock.close()


@pytest.mark.timeout(5)
def test_handle_json_message_and_server():
    received_data = {}
    stop_event = threading.Event()

    def test_handler(data, addr, client_socket):
        received_data['data'] = data
        received_data['addr'] = addr
        client_socket.sendall(b'{"status": "received"}')

    server_thread = threading.Thread(
        target=run_single_connection_json_server,
        args=(9090, test_handler, stop_event),
        daemon=True
    )
    server_thread.start()

    # Wait a bit for server to start
    time.sleep(0.3)

    test_message = {"message": "Hello, Test!"}
    try:
        response = send_json("localhost", 9090, test_message)
    except Exception as e:
        pytest.fail(f"send_json raised an exception: {e}")

    # Wait for server to process message and stop
    stop_event.wait(timeout=3)
    server_thread.join(timeout=1)

    # Assert server received correct data
    assert 'data' in received_data, "Server handler did not receive any data."
    assert received_data['data'] == test_message, (
        f"Server received incorrect data: expected {test_message}, got {received_data['data']}"
    )
    assert 'addr' in received_data, "Server handler did not capture client address."

    assert isinstance(response, dict), f"Response is not a dict: {response}"
    assert response == {"status": "received"}, (
        f"Unexpected response from server: expected {{'status': 'received'}}, got {response}"
    )

    print("[TEST PASSED] JSON server received and responded correctly.")
