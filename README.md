# easy-socket

A simplified socket programming toolkit for Python.

## Features

- TCP/UDP messaging (sync & async)
- JSON socket communication
- File transfer over TCP
- Threaded/multi-client support
- Command-line interface

## Installation

```bash
pip install easy-socket
```

## Usage

```python
from easy_socket import send_tcp_message

send_tcp_message("localhost", 8080, "Hello, World!")
```
