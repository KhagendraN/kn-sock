# Interactive TCP Shell

Use the `knsock interactive` shell to connect to multiple TCP endpoints and test message flows live. This tool is helpful for demos, debugging, and exploring server behavior during development.

!!! note
    Currently supports only TCP. WebSocket or UDP extensions may be added later.

## Features

- Connect to named TCP endpoints
- Send and receive UTF‑8 messages
- Switch between multiple connections
- View message history
- Toggle background receive mode
- Gracefully disconnect or quit

## Commands

| Command         | Description                                        |
|-----------------|----------------------------------------------------|
| `connect`       | Connect to a TCP server and name the connection    |
| `list`          | List all active connections                        |
| `select`        | Choose a default connection for sending/receiving  |
| `send`          | Send a UTF-8 message to the selected connection    |
| `receive`       | Receive a UTF-8 message manually                   |
| `bg_receive`    | Toggle auto-receive mode (runs in background)      |
| `history`       | Show last 10 messages sent/received                |
| `disconnect`    | Close and remove a connection                      |
| `quit` / `exit` | Exit the shell and close all connections           |
| `help`          | Show command help                                  |

## How to Launch

```bash
python3 -m kn_sock.interactive_cli
```

## Before You Start

The interactive CLI connects to existing TCP servers. To test it locally, start a simple TCP echo server using the Python API:

```python
# echo_server.py
from kn_sock import start_tcp_server

def echo(conn, addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(b"Echo: " + data)

start_tcp_server(9000, echo)
```

Run it in a separate terminal:

```bash
python3 echo_server.py
```

Now launch the CLI:

```bash
python3 -m kn_sock.interactive_cli
```

And try:

```
(kn-sock) connect local 127.0.0.1 9000
(kn-sock) send hello
(kn-sock) receive
```

## Example Session

```
(kn-sock) connect local 127.0.0.1 9000
Connected to 127.0.0.1:9000 as "local".

(kn-sock) send Hello TCP
Message sent.

(kn-sock) receive
Received: Echo: Hello TCP

(kn-sock) quit
Exiting kn-sock interactive CLI.
```

## When to Use

Use the interactive shell when you want to:

- Manually test one or more TCP endpoints
- Observe live message exchange
- Run quick ad hoc experiments during QA
- Demonstrate app behavior during dev sessions

## Related Pages

- TCP Python API
- TCP CLI Reference
- TCP Testing