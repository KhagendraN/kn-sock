# File Transfer Utilities

kn-sock includes utilities for sending and receiving files over TCP—ideal for quick one-off transfers, automation, or as a building block for larger workflows.

## CLI Commands

### 1. Start a File Receiver Server

Launch a TCP server that receives and saves incoming files to a specified directory.

| Command                                          | Description                                  |
|--------------------------------------------------|----------------------------------------------|
| `run-file-server <port> <save_dir>`              | Start a TCP file receiver                    |

**Example:**
```sh
docker-compose run --rm knsock run-file-server 7001 /tmp/incoming
# Or: knsock run-file-server 7001 /tmp/incoming
```
**Output:**
```
[FILE][SERVER] Listening on 0.0.0.0:7001
[FILE][SERVER] Saving received files to /tmp/incoming
```

### 2. Send a File

Send a file to a TCP file receiver server.

| Command                                       | Description                   |
|-----------------------------------------------|-------------------------------|
| `send-file <host> <port> <filepath>`          | Send a file over TCP          |

**Example:**
```sh
docker-compose run --rm knsock send-file 172.18.0.2 7001 ./README.md
```
**Output:**
```
[FILE][CLIENT] Sent file: ./README.md to 172.18.0.2:7001
```

#### Options Table
| Option        | Description                           |
|---------------|---------------------------------------|
| `<port>`      | Port number for server/client         |
| `<host>`      | IP or hostname of server (for client) |
| `<filepath>`  | Path to file to send (client)        |
| `<save_dir>`  | Directory to save received files (server) |

## Python API

### Start a File Server
```python
from kn_sock import start_file_server

start_file_server(7001, save_dir="/tmp/incoming")
```

### Send a File
```python
from kn_sock import send_file

send_file("127.0.0.1", 7001, "./README.md")
```

### Sample Output
**Server terminal:**
```
[FILE][SERVER] Listening on 0.0.0.0:7001
[FILE][SERVER] Saving received files to /tmp/incoming
[FILE][SERVER] Received file: README.md from ('172.18.0.1', 59923)
```

**Client terminal:**
```
[FILE][CLIENT] Sent file: ./README.md to 172.18.0.2:7001
```

## Known Issues & Troubleshooting
| Issue                        | Symptom/Output                              | Solution                                           |
|------------------------------|---------------------------------------------|----------------------------------------------------|
| File not saved               | No file appears in save_dir                 | Check write permissions on server directory        |
| File too large / incomplete  | Partial file or error                       | Check network stability and disk space             |
| Port already in use          | `[Errno 98] Address in use`                 | Use a different port or stop other processes       |
| Hostname not found           | `[Errno -2] Name or service not known`      | Use container IP in Docker setups                  |

## Testing
### Manual Test
Start the file server:
```sh
docker-compose run --rm knsock run-file-server 7001 /tmp/incoming
```

In another terminal, send a file:
```sh
docker-compose run --rm knsock send-file <server-ip> 7001 ./README.md
# Example: send-file 172.18.0.2 7001 ./README.md
```

Check `/tmp/incoming` in the container for the transferred file.