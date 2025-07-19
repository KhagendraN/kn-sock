import pytest
import time
from unittest.mock import patch, Mock
from kn_sock.decorators import log_exceptions, retry, measure_time, ensure_json_input


### log_exceptions TEST ###
def test_log_exceptions_logs_and_raises(caplog):
    @log_exceptions(raise_error=True)
    def faulty_handler(data, addr, client_socket):
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        faulty_handler(b"data", ("127.0.0.1", 12345), Mock())

    assert any("Test error" in record.message for record in caplog.records)


### retry TEST ###
def test_retry_retries_and_succeeds():
    attempts = {"count": 0}

    @retry(retries=3, delay=0.1, exceptions=(ValueError,))
    def flaky_handler(data, addr, client_socket):
        if attempts["count"] < 2:
            attempts["count"] += 1
            raise ValueError("Temporary failure")
        return "success"

    result = flaky_handler(b"data", ("127.0.0.1", 12345), Mock())
    assert result == "success"
    assert attempts["count"] == 2


### measure_time TEST ###
def test_measure_time_output(capsys):
    @measure_time
    def dummy_handler(data, addr, client_socket):
        time.sleep(0.05)
        return "done"

    result = dummy_handler(b"data", ("127.0.0.1", 12345), Mock())
    captured = capsys.readouterr()
    assert "Execution time" in captured.out
    assert result == "done"


### ensure_json_input TEST ###
def test_ensure_json_input_accepts_dict():
    @ensure_json_input
    def json_handler(data, addr, client_socket):
        return data["key"]

    result = json_handler({"key": "value"}, ("127.0.0.1", 12345), Mock())
    assert result == "value"


def test_ensure_json_input_accepts_valid_json_string():
    @ensure_json_input
    def json_handler(data, addr, client_socket):
        return data["key"]

    result = json_handler('{"key": "value"}', ("127.0.0.1", 12345), Mock())
    assert result == "value"


def test_ensure_json_input_raises_on_invalid_json():
    @ensure_json_input
    def json_handler(data, addr, client_socket):
        return data

    with pytest.raises(Exception):
        json_handler("not a json", ("127.0.0.1", 12345), Mock())
