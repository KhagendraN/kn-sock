# Interactive TCP Shell

Use the `knsock interactive` shell to connect to multiple TCP endpoints and test message flows live. This tool is helpful for demos, debugging, and exploring server behavior during development.

!!! note
    Currently supports only [TCP](../tcp/index.md). WebSocket or UDP extensions may be added later.

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

The interactive CLI connects to existing TCP servers.
To test it locally, create a simple TCP echo server using the Python API:

```python
# echo_server.py
from kn_sock import start_tcp_server

def echo(data, addr, conn):
    print(f"Connection from {addr}")
    try:
        print(f"Received: {data}")
        conn.sendall(b"Echo: " + data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        print(f"Closed connection to {addr}")

start_tcp_server(9001, echo, host="0.0.0.0")
```
!!! note
    You can also use the prebuilt `echo_server.py` file included in the project root for testing. It uses the same handler function shown above and listens on port 9001.

Run it in a separate terminal:

```bash
python3 echo_server.py
```

Then launch the interactive CLI in another terminal:

```bash
python3 -m kn_sock.interactive_cli
```

And try the following:

```perl
(kn-sock) connect local 127.0.0.1 9001
(kn-sock) send hello
(kn-sock) receive
```

## Example Session

```pgsql
(kn-sock) connect local 127.0.0.1 9001
Connected to 127.0.0.1:9001 as "local".

(kn-sock) send hello
Message sent.

(kn-sock) receive
Received: Echo: hello

(kn-sock) quit
Exiting kn-sock interactive CLI.
```

!!! info
    The `echo_server.py` handler closes the connection after replying. For persistent sessions, modify the handler to keep the connection open.

## When to Use

Use the interactive shell when you want to:

- Manually test one or more TCP endpoints
- Observe live message exchange
- Run quick ad hoc experiments during QA
- Demonstrate app behavior during dev sessions

## Related Pages

- [TCP Python API](../tcp/python-api.md)
- [TCP CLI Reference](../tcp/cli.md)
- [TCP Testing](../tcp/testing.md)