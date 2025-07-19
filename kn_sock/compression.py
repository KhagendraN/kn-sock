"""
kn_sock.compression

Provides gzip and deflate compression utilities for large messages.

Usage:
    from kn_sock.compression import compress_data, decompress_data, detect_compression
    compressed = compress_data(data, method='gzip')
    original = decompress_data(compressed)

Supported methods: 'gzip', 'deflate'.
"""
import gzip
import zlib


def compress_data(data: bytes, method: str = "gzip") -> bytes:
    """Compress data using gzip or deflate."""
    if method == "gzip":
        return gzip.compress(data)
    elif method == "deflate":
        return zlib.compress(data)
    else:
        raise ValueError(f"Unsupported compression method: {method}")


def decompress_data(data: bytes) -> bytes:
    """Decompress data (auto-detect gzip or deflate)."""
    if data[:2] == b"\x1f\x8b":  # gzip magic
        return gzip.decompress(data)
    try:
        return zlib.decompress(data)
    except zlib.error:
        raise ValueError("Unknown or unsupported compression format.")


def detect_compression(data: bytes) -> str:
    """Detect compression type ('gzip', 'deflate', or 'none')."""
    if data[:2] == b"\x1f\x8b":
        return "gzip"
    try:
        zlib.decompress(data)
        return "deflate"
    except zlib.error:
        return "none"
