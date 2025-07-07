# kn_sock/errors.py

class EasySocketError(Exception):
    """Base exception for all easy_socket errors."""
    pass

# -----------------------------
# Connection-related errors
# -----------------------------

class ConnectionTimeoutError(EasySocketError):
    """Raised when a connection or read/write operation times out."""
    def __init__(self, message="Connection timed out."):
        super().__init__(message)

class PortInUseError(EasySocketError):
    """Raised when a specified port is already in use."""
    def __init__(self, port, message=None):
        message = message or f"Port {port} is already in use."
        super().__init__(message)

# -----------------------------
# Data & Protocol errors
# -----------------------------

class InvalidJSONError(EasySocketError):
    """Raised when a JSON message cannot be decoded."""
    def __init__(self, message="Received invalid JSON data."):
        super().__init__(message)

class UnsupportedProtocolError(EasySocketError):
    """Raised when a requested protocol is not supported."""
    def __init__(self, protocol, message=None):
        message = message or f"Protocol '{protocol}' is not supported."
        super().__init__(message)

# -----------------------------
# File transfer errors
# -----------------------------

class FileTransferError(EasySocketError):
    """Raised when file transfer fails."""
    def __init__(self, message="File transfer failed."):
        super().__init__(message)
