# kn_sock/__init__.py

"""
kn_sock
-----------
A simplified socket programming toolkit for Python.

Features:
- TCP/UDP messaging (sync & async)
- JSON socket communication
- File transfer over TCP
- Threaded/multi-client support
- Command-line interface
- Multi-client video chat with voice and text
"""

__version__ = "0.1.0"
__author__ = "Khagendra Neupane"
__license__ = "MIT"

import logging


def configure_logging(level=logging.INFO, fmt=None):
    """Configure kn_sock logging globally."""
    if fmt is None:
        fmt = "[%(levelname)s][%(name)s] %(message)s"
    logging.basicConfig(level=level, format=fmt, force=True)


# Set default logging config on import
configure_logging()

# Only import and expose public API symbols that are actually used. Remove unused imports and fix E402 errors by placing imports at the top.
from .tcp import (
    send_tcp_message,
    send_tcp_bytes,
    start_tcp_server,
    start_threaded_tcp_server,
    start_async_tcp_server,
    send_tcp_message_async,
    start_ssl_tcp_server,
    send_ssl_tcp_message,
    start_async_ssl_tcp_server,
    send_ssl_tcp_message_async,
    TCPConnectionPool,
)
from .udp import (
    send_udp_message,
    start_udp_server,
    send_udp_message_async,
    start_udp_server_async,
    send_udp_multicast,
    start_udp_multicast_server,
)
from .file_transfer import (
    send_file,
    start_file_server,
    send_file_async,
    start_file_server_async,
)
from .json_socket import (
    start_json_server,
    send_json,
    start_json_server_async,
    send_json_async,
    send_json_response,
    send_json_response_async,
)
from .utils import *
from .errors import *

# Optional import for live_stream (requires cv2, pyaudio)
try:
    from .live_stream import start_live_stream, connect_to_live_server
except ImportError:
    # Define placeholder functions that raise informative errors
    def start_live_stream(*args, **kwargs):
        raise ImportError("live_stream functionality requires additional dependencies. Install with: pip install opencv-python pyaudio")
    
    def connect_to_live_server(*args, **kwargs):
        raise ImportError("live_stream functionality requires additional dependencies. Install with: pip install opencv-python pyaudio")

from .websocket import (
    start_websocket_server,
    start_async_websocket_server,
    connect_websocket,
    async_connect_websocket,
    AsyncWebSocketConnection,
)
from .http import http_get, http_post, https_get, https_post, start_http_server
from .pubsub import start_pubsub_server, PubSubClient
from .rpc import start_rpc_server, RPCClient

# Optional import for video_chat (requires cv2, pyaudio)  
try:
    from .video_chat import VideoChatServer, VideoChatClient
except ImportError:
    # Define placeholder classes that raise informative errors
    class VideoChatServer:
        def __init__(self, *args, **kwargs):
            raise ImportError("video_chat functionality requires additional dependencies. Install with: pip install opencv-python pyaudio")
    
    class VideoChatClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("video_chat functionality requires additional dependencies. Install with: pip install opencv-python pyaudio")

from .compression import compress_data, decompress_data, detect_compression
from .decorators import log_exceptions, retry, measure_time, ensure_json_input
from .interactive_cli import KnSockInteractiveCLI
from .network import arp_scan, mac_lookup, monitor_dns
