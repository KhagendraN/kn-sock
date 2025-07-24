"""
kn_sock.load_balancer

Load balancing utilities: round-robin and least-connections algorithms.

Usage:
    from kn_sock.load_balancer import RoundRobinLoadBalancer, LeastConnectionsLoadBalancer
    lb = RoundRobinLoadBalancer()
    lb.add_server('127.0.0.1:9000')
    lb.add_server('127.0.0.1:9001')
    server = lb.get_server()

    lcb = LeastConnectionsLoadBalancer()
    lcb.add_server('127.0.0.1:9000')
    lcb.update_connections('127.0.0.1:9000', 2)
    server = lcb.get_server()

Both support add_server, remove_server, get_server, and (for least-connections) update_connections.
"""
import threading

class RoundRobinLoadBalancer:
    def __init__(self):
        self.servers = []
        self.index = 0
        self.lock = threading.Lock()

    def add_server(self, server):
        with self.lock:
            if server not in self.servers:
                self.servers.append(server)

    def remove_server(self, server):
        with self.lock:
            if server in self.servers:
                idx = self.servers.index(server)
                self.servers.remove(server)
                if idx <= self.index and self.index > 0:
                    self.index -= 1

    def get_server(self):
        with self.lock:
            if not self.servers:
                raise RuntimeError("No servers available")
            server = self.servers[self.index % len(self.servers)]
            self.index = (self.index + 1) % len(self.servers)
            return server

class LeastConnectionsLoadBalancer:
    def __init__(self):
        self.servers = {}
        self.lock = threading.Lock()

    def add_server(self, server):
        with self.lock:
            if server not in self.servers:
                self.servers[server] = 0

    def remove_server(self, server):
        with self.lock:
            if server in self.servers:
                del self.servers[server]

    def update_connections(self, server, count):
        with self.lock:
            if server in self.servers:
                self.servers[server] = count

    def get_server(self):
        with self.lock:
            if not self.servers:
                raise RuntimeError("No servers available")
            # Return server with fewest connections
            return min(self.servers, key=lambda s: self.servers[s]) 