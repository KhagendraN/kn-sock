# easy_socket/__init__.py

"""
easy_socket
-----------
A simplified socket programming toolkit for Python.

Features:
- TCP/UDP messaging (sync & async)
- JSON socket communication
- File transfer over TCP
- Threaded/multi-client support
- Command-line interface
"""

__version__ = "0.1.0"
__author__ = "Khagendra Neupane"
__license__ = "MIT"

# TCP
from .tcp import (
    send_tcp_message,
    start_tcp_server,
    start_tcp_server_threaded,
    start_tcp_server_async,
    send_tcp_message_async
)

# UDP
from .udp import (
    send_udp_message,
    start_udp_server,
    send_udp_message_async,
    start_udp_server_async
)

# File Transfer
from .file_transfer import (
    send_file,
    start_file_server,
    send_file_async,
    start_file_server_async
)

# JSON Socket
from .json_socket import (
    JsonSocketServer,
    JsonSocketClient,
    AsyncJsonSocketServer,
    AsyncJsonSocketClient
)

# Utilities & Errors
from . import utils
from . import errors
