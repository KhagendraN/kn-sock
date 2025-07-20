"""
kn_sock.config

Configuration file support for kn_sock. Allows loading default settings (host, port, SSL, etc.) from JSON or YAML files.

Usage:
    from kn_sock.config import load_config, get_config, set_config
    load_config('config.json')
    host = get_config('host', '127.0.0.1')

Supports JSON (.json) and YAML (.yaml/.yml) files.
"""
import os
import json
from typing import Any, Optional

try:
    import yaml

    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

_CONFIG = {}


def load_config(path: str) -> None:
    """Load configuration from a JSON or YAML file."""
    global _CONFIG
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    with open(path, "r") as f:
        if ext == ".json":
            _CONFIG = json.load(f)
        elif ext in (".yaml", ".yml"):
            if not _HAS_YAML:
                raise ImportError(
                    "PyYAML is required for YAML config files. Install with 'pip install pyyaml'."
                )
            _CONFIG = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config file type: {ext}")


def get_config(key: str, default: Optional[Any] = None) -> Any:
    """Get a config value by key, or return default if not set."""
    return _CONFIG.get(key, default)


def set_config(key: str, value: Any) -> None:
    """Set a config value at runtime."""
    _CONFIG[key] = value


def merge_with_args(args: dict) -> dict:
    """Merge config values with CLI args (args take precedence)."""
    merged = dict(_CONFIG)
    merged.update({k: v for k, v in args.items() if v is not None})
    return merged
