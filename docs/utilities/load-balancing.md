# Load Balancing

Load balancing algorithms for distributing connections across multiple servers.

## Classes

### `RoundRobinLoadBalancer`
Distributes requests in round-robin order.

**Methods:**
- `add_server(server)` - Add a server
- `remove_server(server)` - Remove a server  
- `get_server()` - Get next server in rotation

**Example:**
```python
from kn_sock.load_balancer import RoundRobinLoadBalancer

lb = RoundRobinLoadBalancer()
lb.add_server('127.0.0.1:9000')
lb.add_server('127.0.0.1:9001')
lb.add_server('127.0.0.1:9002')

# Get servers in rotation
server1 = lb.get_server()  # Returns '127.0.0.1:9000'
server2 = lb.get_server()  # Returns '127.0.0.1:9001'
server3 = lb.get_server()  # Returns '127.0.0.1:9002'
server4 = lb.get_server()  # Returns '127.0.0.1:9000' (cycles)
```

### `LeastConnectionsLoadBalancer`
Routes to server with fewest active connections.

**Methods:**
- `add_server(server)` - Add a server
- `remove_server(server)` - Remove a server
- `update_connections(server, count)` - Update connection count
- `get_server()` - Get server with fewest connections

**Example:**
```python
from kn_sock.load_balancer import LeastConnectionsLoadBalancer

lb = LeastConnectionsLoadBalancer()
lb.add_server('127.0.0.1:9000')
lb.add_server('127.0.0.1:9001')

# Update connection counts
lb.update_connections('127.0.0.1:9000', 5)
lb.update_connections('127.0.0.1:9001', 2)

server = lb.get_server()  # Returns '127.0.0.1:9001' (fewer connections)
```

## Usage with TCP Servers

```python
from kn_sock.load_balancer import RoundRobinLoadBalancer
import socket

lb = RoundRobinLoadBalancer()
lb.add_server('backend1:8080')
lb.add_server('backend2:8080')

def forward_request(data, addr, client_socket):
    # Get next backend server
    backend = lb.get_server()
    host, port = backend.split(':')
    
    # Forward to backend
    with socket.socket() as backend_sock:
        backend_sock.connect((host, int(port)))
        backend_sock.send(data)
        response = backend_sock.recv(1024)
        client_socket.send(response)
```
