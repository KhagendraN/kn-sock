# RPC Utilities

kn-sock includes simple remote procedure call (RPC) utilities to demonstrate calling functions on remote servers for use in basic microservices, distributed testing, or automation.

## CLI Commands

### 1. Start an RPC Server

Run a server that exposes simple functions (e.g., add, echo) to remote clients.

| Command                               | Description              |
|----------------------------------------|--------------------------|
| `run-rpc-server <port>`                | Start an RPC server      |

**Example:**
```sh
docker-compose run --rm knsock run-rpc-server 9200
# Or: knsock run-rpc-server 9200
```
**Output:**
```
[RPC][SERVER] Listening on 0.0.0.0:9200
```

### 2. Connect as an RPC Client

Invoke a remote function exposed by the server (e.g., add, echo).

| Command                                       | Description                   |
|-----------------------------------------------|-------------------------------|
| `rpc-client <host> <port> <function> [args...]` | Call remote function via RPC |

**Example:**
```sh
docker-compose run --rm knsock rpc-client 172.18.0.2 9200 add 2 3
```
**Output:**
```
[RPC][CLIENT] add(2, 3) → 5
```

Or, to echo a string:
```sh
docker-compose run --rm knsock rpc-client 172.18.0.2 9200 echo "hello"
```
**Output:**
```
[RPC][CLIENT] echo('hello') → 'hello'
```

#### Options Table
| Option        | Description                           |
|---------------|---------------------------------------|
| `<port>`      | Port for server/client               |
| `<host>`      | IP/hostname of server (client only)  |
| `<function>`  | Function to call (e.g., add, echo)   |
| `[args...]`   | Arguments for the remote function (space-separated) |

## Python API

### Start an RPC Server
```python
from kn_sock import start_rpc_server

start_rpc_server(9200)
```

### Call as an RPC Client
```python
from kn_sock import RPCClient

client = RPCClient('127.0.0.1', 9200)
print(client.call('add', 2, 3))  # → 5
print(client.call('echo', 'hello'))  # → 'hello'
```

### Sample Output
**Server terminal:**
```
[RPC][SERVER] Listening on 0.0.0.0:9200
[RPC][SERVER] Received call: add(2, 3) from ('172.18.0.1', 60222)
```

**Client terminal:**
```
[RPC][CLIENT] add(2, 3) → 5
[RPC][CLIENT] echo('hello') → 'hello'
```

## Known Issues & Troubleshooting
| Issue                        | Symptom/Output                              | Solution                                           |
|------------------------------|---------------------------------------------|----------------------------------------------------|
| Function not found           | Error: function not implemented             | Use only supported functions (add, echo)           |
| Connection refused           | `ConnectionRefusedError`                    | Ensure server is running                           |
| Hostname not found           | `[Errno -2] Name or service not known`      | Use container IP for Docker setups                 |

## Testing
### Manual Test
Start the RPC server:
```sh
docker-compose run --rm knsock run-rpc-server 9200
```

In another terminal, call a function:
```sh
docker-compose run --rm knsock rpc-client <server-ip> 9200 add 2 3
# Example: rpc-client 172.18.0.2 9200 add 2 3
```

Try another function:
```sh
docker-compose run --rm knsock rpc-client <server-ip> 9200 echo "test"
```

You should see results printed for each call.