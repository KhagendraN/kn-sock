import pytest

from kn_sock.errors import (
    EasySocketError,
    ConnectionTimeoutError,
    PortInUseError,
    InvalidJSONError,
    UnsupportedProtocolError,
    FileTransferError,
)

### EasySocketError ###
def test_easy_socket_error():
    try:
        raise EasySocketError("General socket error")
    except EasySocketError as e:
        assert isinstance(e, EasySocketError)
        assert str(e) == "General socket error"
        print("[SUCCESS] EasySocketError raised and caught successfully.")

### ConnectionTimeoutError ###
def test_connection_timeout_error():
    try:
        raise ConnectionTimeoutError("Connection timed out")
    except ConnectionTimeoutError as e:
        assert isinstance(e, ConnectionTimeoutError)
        assert str(e) == "Connection timed out"
        print("[SUCCESS] ConnectionTimeoutError raised and caught successfully.")

### PortInUseError ###
def test_port_in_use_error():
    try:
        raise PortInUseError(5000)
    except PortInUseError as e:
        assert isinstance(e, PortInUseError)
        assert str(e) == "Port 5000 is already in use."
        print("[SUCCESS] PortInUseError raised and caught successfully.")

### UnsupportedProtocolError ###
def test_unsupported_protocol_error():
    try:
        raise UnsupportedProtocolError("XYZ")
    except UnsupportedProtocolError as e:
        assert isinstance(e, UnsupportedProtocolError)
        assert str(e) == "Protocol 'XYZ' is not supported."
        print("[SUCCESS] UnsupportedProtocolError raised and caught successfully.")

### InvalidJSONError ###
def test_invalid_json_error():
    try:
        raise InvalidJSONError("Invalid JSON data")
    except InvalidJSONError as e:
        assert isinstance(e, InvalidJSONError)
        assert str(e) == "Invalid JSON data"
        print("[SUCCESS] InvalidJSONError raised and caught successfully.")


### FileTransferError ###
def test_file_transfer_error():
    try:
        raise FileTransferError("File transfer failed")
    except FileTransferError as e:
        assert isinstance(e, FileTransferError)
        assert str(e) == "File transfer failed"
        print("[SUCCESS] FileTransferError raised and caught successfully.")
