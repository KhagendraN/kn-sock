import pytest
import time
import logging
import io
import contextlib
from kn_sock.decorators import log_exceptions, retry, measure_time, ensure_json_input
from kn_sock.errors import InvalidJSONError


def test_log_exceptions_raises():
    @log_exceptions(raise_error=True)
    def fail():
        raise ValueError("fail!")

    with pytest.raises(ValueError):
        fail()


def test_log_exceptions_no_raise():
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger("kn_sock.decorators")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    @log_exceptions(raise_error=False)
    def fail():
        raise ValueError("fail!")

    try:
        fail()
    except Exception:
        pass
    handler.flush()
    output = log_stream.getvalue()
    logger.removeHandler(handler)
    assert "Exception in 'fail': fail!" in output


def test_retry_retries(monkeypatch):
    calls = {"n": 0}

    @retry(retries=3, delay=0.01, exceptions=(ValueError,))
    def sometimes_fails():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("fail")
        return "ok"

    assert sometimes_fails() == "ok"
    assert calls["n"] == 3


def test_measure_time():
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger("kn_sock.decorators")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    @measure_time
    def slow():
        import time

        time.sleep(0.01)

    slow()
    handler.flush()
    output = log_stream.getvalue()
    logger.removeHandler(handler)
    assert "[TIMER]" in output


def test_ensure_json_input_accepts_dict():
    @ensure_json_input
    def handler(data):
        return data

    assert handler({"a": 1}) == {"a": 1}


def test_ensure_json_input_accepts_json_str():
    @ensure_json_input
    def handler(data):
        return data

    assert handler('{"a": 1}') == {"a": 1}


def test_ensure_json_input_rejects_invalid():
    @ensure_json_input
    def handler(data):
        return data

    with pytest.raises(InvalidJSONError):
        handler("not json")
    with pytest.raises(InvalidJSONError):
        handler(123)
