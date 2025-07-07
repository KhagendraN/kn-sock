import pytest
import time
from kn_sock.decorators import log_exceptions, retry, measure_time, ensure_json_input
from kn_sock.errors import InvalidJSONError

def test_log_exceptions_raises():
    @log_exceptions(raise_error=True)
    def fail():
        raise ValueError('fail!')
    with pytest.raises(ValueError):
        fail()

def test_log_exceptions_no_raise(capsys):
    @log_exceptions(raise_error=False)
    def fail():
        raise ValueError('fail!')
    fail()
    out = capsys.readouterr().out
    assert '[ERROR]' in out

def test_retry_retries(monkeypatch):
    calls = {'n': 0}
    @retry(retries=3, delay=0.01, exceptions=(ValueError,))
    def sometimes_fails():
        calls['n'] += 1
        if calls['n'] < 3:
            raise ValueError('fail')
        return 'ok'
    assert sometimes_fails() == 'ok'
    assert calls['n'] == 3

def test_measure_time(capsys):
    @measure_time
    def slow():
        time.sleep(0.01)
        return 42
    result = slow()
    out = capsys.readouterr().out
    assert '[TIMER]' in out
    assert result == 42

def test_ensure_json_input_accepts_dict():
    @ensure_json_input
    def handler(data):
        return data
    assert handler({'a': 1}) == {'a': 1}

def test_ensure_json_input_accepts_json_str():
    @ensure_json_input
    def handler(data):
        return data
    assert handler('{"a": 1}') == {'a': 1}

def test_ensure_json_input_rejects_invalid():
    @ensure_json_input
    def handler(data):
        return data
    with pytest.raises(InvalidJSONError):
        handler('not json')
    with pytest.raises(InvalidJSONError):
        handler(123) 