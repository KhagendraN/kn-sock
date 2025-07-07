# kn_sock/decorators.py

import time
import json
import functools
import traceback
from typing import Callable, Any, Optional, Type
from kn_sock.errors import InvalidJSONError


# -----------------------------
# 🧾 Log Exceptions
# -----------------------------

def log_exceptions(raise_error: bool = True):
    """
    Logs exceptions and optionally re-raises them.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[ERROR] Exception in '{func.__name__}': {e}")
                traceback.print_exc()
                if raise_error:
                    raise
        return wrapper
    return decorator


# -----------------------------
# 🔁 Retry Decorator
# -----------------------------

def retry(
    retries: int = 3,
    delay: float = 1.0,
    exceptions: tuple = (Exception,)
):
    """
    Retries a function upon failure, with delay.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"[RETRY] {func.__name__}: Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator


# -----------------------------
# ⏱️ Measure Execution Time
# -----------------------------

def measure_time(func: Callable):
    """
    Measures and prints execution time of the wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[TIMER] {func.__name__} executed in {elapsed:.4f} seconds")
        return result
    return wrapper


# -----------------------------
# ✅ Ensure JSON Input
# -----------------------------

def ensure_json_input(func: Callable):
    """
    Validates that the first argument is a valid JSON object (dict or str).
    Raises InvalidJSONError otherwise.
    """
    @functools.wraps(func)
    def wrapper(data, *args, **kwargs):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                raise InvalidJSONError("Handler received invalid JSON string.")
        elif not isinstance(data, dict):
            raise InvalidJSONError("Handler expects JSON object or string.")

        return func(data, *args, **kwargs)
    return wrapper
