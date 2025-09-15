# Remote Procedure Calls (RPC)

kn-sock provides a comprehensive RPC system that allows you to call functions on remote servers as if they were local, with support for both synchronous and asynchronous operations.

## Overview

RPC features in kn-sock:
- **Transparent remote calls**: Call remote functions like local functions
- **Multiple serialization formats**: JSON, Protocol Buffers, and custom serializers
- **Async and sync support**: Both synchronous and asynchronous RPC calls
- **Error handling**: Automatic exception propagation across network
- **Authentication**: Built-in authentication and authorization
- **Load balancing**: Distribute calls across multiple servers
- **Middleware support**: Custom preprocessing and postprocessing
- **Service discovery**: Automatic server discovery and registration

## Basic RPC Usage

### RPC Server

```python
from kn_sock import RPCServer

class MathService:
    """Example RPC service with mathematical operations."""
    
    def add(self, a, b):
        """Add two numbers."""
        return a + b
    
    def subtract(self, a, b):
        """Subtract two numbers."""
        return a - b
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a, b):
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b
    
    def factorial(self, n):
        """Calculate factorial of a number."""
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n == 0 or n == 1:
            return 1
        
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

def basic_rpc_server():
    """Start a basic RPC server."""
    
    # Create RPC server
    server = RPCServer(host='0.0.0.0', port=8080)
    
    # Register service
    math_service = MathService()
    server.register_service('math', math_service)
    
    # Register individual functions
    def hello(name):
        return f"Hello, {name}!"
    
    def get_server_time():
        import datetime
        return datetime.datetime.now().isoformat()
    
    server.register_function('hello', hello)
    server.register_function('get_time', get_server_time)
    
    print("RPC Server started on localhost:8080")
    print("Available services:")
    print("  - math.add(a, b)")
    print("  - math.subtract(a, b)")
    print("  - math.multiply(a, b)")
    print("  - math.divide(a, b)")
    print("  - math.factorial(n)")
    print("  - hello(name)")
    print("  - get_time()")
    
    # Start the server
    server.start()

if __name__ == "__main__":
    basic_rpc_server()
```

### RPC Client

```python
from kn_sock import RPCClient

def basic_rpc_client():
    """Example RPC client."""
    
    # Connect to RPC server
    client = RPCClient('localhost', 8080)
    
    try:
        # Call individual functions
        greeting = client.call('hello', 'Alice')
        print(f"Greeting: {greeting}")
        
        server_time = client.call('get_time')
        print(f"Server time: {server_time}")
        
        # Call service methods
        result = client.call('math.add', 10, 20)
        print(f"10 + 20 = {result}")
        
        result = client.call('math.multiply', 7, 8)
        print(f"7 * 8 = {result}")
        
        result = client.call('math.factorial', 5)
        print(f"5! = {result}")
        
        # Handle errors
        try:
            result = client.call('math.divide', 10, 0)
        except Exception as e:
            print(f"Error: {e}")
        
        # Batch calls
        batch_results = client.batch_call([
            ('math.add', [1, 2]),
            ('math.multiply', [3, 4]),
            ('hello', ['Bob'])
        ])
        
        print(f"Batch results: {batch_results}")
        
    finally:
        client.close()

if __name__ == "__main__":
    basic_rpc_client()
```

## Asynchronous RPC

### Async RPC Server

```python
import asyncio
from kn_sock import AsyncRPCServer

class AsyncDatabaseService:
    """Example async RPC service simulating database operations."""
    
    def __init__(self):
        self.data = {}
    
    async def get(self, key):
        """Get value by key."""
        # Simulate database delay
        await asyncio.sleep(0.1)
        return self.data.get(key)
    
    async def set(self, key, value):
        """Set key-value pair."""
        # Simulate database delay
        await asyncio.sleep(0.05)
        self.data[key] = value
        return True
    
    async def delete(self, key):
        """Delete key."""
        await asyncio.sleep(0.05)
        return self.data.pop(key, None)
    
    async def list_keys(self):
        """List all keys."""
        await asyncio.sleep(0.1)
        return list(self.data.keys())
    
    async def bulk_set(self, items):
        """Set multiple key-value pairs."""
        await asyncio.sleep(0.1)
        for key, value in items.items():
            self.data[key] = value
        return len(items)

async def async_rpc_server():
    """Start an async RPC server."""
    
    # Create async RPC server
    server = AsyncRPCServer(host='0.0.0.0', port=8081)
    
    # Register async service
    db_service = AsyncDatabaseService()
    server.register_service('db', db_service)
    
    # Register async functions
    async def async_hello(name):
        await asyncio.sleep(0.1)  # Simulate async work
        return f"Async hello, {name}!"
    
    async def fetch_data(url):
        """Simulate fetching data from URL."""
        await asyncio.sleep(0.5)  # Simulate network delay
        return f"Data from {url}: [simulated response]"
    
    server.register_function('async_hello', async_hello)
    server.register_function('fetch_data', fetch_data)
    
    print("Async RPC Server started on localhost:8081")
    print("Available async services:")
    print("  - db.get(key)")
    print("  - db.set(key, value)")
    print("  - db.delete(key)")
    print("  - db.list_keys()")
    print("  - db.bulk_set(items)")
    print("  - async_hello(name)")
    print("  - fetch_data(url)")
    
    # Start the server
    await server.start()

if __name__ == "__main__":
    asyncio.run(async_rpc_server())
```

### Async RPC Client

```python
import asyncio
from kn_sock import AsyncRPCClient

async def async_rpc_client():
    """Example async RPC client."""
    
    # Connect to async RPC server
    client = AsyncRPCClient('localhost', 8081)
    
    try:
        # Async function calls
        greeting = await client.call('async_hello', 'Alice')
        print(f"Async greeting: {greeting}")
        
        # Database operations
        await client.call('db.set', 'user:1', {'name': 'John', 'age': 30})
        await client.call('db.set', 'user:2', {'name': 'Jane', 'age': 25})
        
        user1 = await client.call('db.get', 'user:1')
        print(f"User 1: {user1}")
        
        keys = await client.call('db.list_keys')
        print(f"All keys: {keys}")
        
        # Bulk operations
        bulk_data = {
            'product:1': {'name': 'Laptop', 'price': 999},
            'product:2': {'name': 'Mouse', 'price': 25},
            'product:3': {'name': 'Keyboard', 'price': 75}
        }
        
        items_set = await client.call('db.bulk_set', bulk_data)
        print(f"Bulk set {items_set} items")
        
        # Concurrent calls
        tasks = [
            client.call('fetch_data', 'https://api1.example.com'),
            client.call('fetch_data', 'https://api2.example.com'),
            client.call('fetch_data', 'https://api3.example.com')
        ]
        
        results = await asyncio.gather(*tasks)
        for i, result in enumerate(results, 1):
            print(f"Concurrent call {i}: {result}")
        
        # Async batch calls
        batch_results = await client.batch_call([
            ('db.get', ['user:1']),
            ('db.get', ['user:2']),
            ('async_hello', ['Bob'])
        ])
        
        print(f"Async batch results: {batch_results}")
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(async_rpc_client())
```

## Advanced RPC Features

### RPC with Authentication

```python
import hashlib
import hmac
import time
from kn_sock import RPCServer, RPCClient

class AuthenticatedRPCServer(RPCServer):
    """RPC server with authentication support."""
    
    def __init__(self, host, port, secret_key):
        super().__init__(host, port)
        self.secret_key = secret_key
        self.authenticated_clients = {}
        self.session_timeout = 3600  # 1 hour
    
    def authenticate_client(self, token, timestamp, signature):
        """Authenticate client using HMAC signature."""
        
        # Check timestamp (prevent replay attacks)
        current_time = time.time()
        if abs(current_time - timestamp) > 300:  # 5 minutes tolerance
            return False, "Token expired"
        
        # Verify HMAC signature
        expected_signature = hmac.new(
            self.secret_key.encode(),
            f"{token}:{timestamp}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            return False, "Invalid signature"
        
        # Store authenticated client
        self.authenticated_clients[token] = {
            "authenticated_at": current_time,
            "last_activity": current_time
        }
        
        return True, "Authentication successful"
    
    def is_authenticated(self, token):
        """Check if client is authenticated."""
        if token not in self.authenticated_clients:
            return False
        
        client_info = self.authenticated_clients[token]
        current_time = time.time()
        
        # Check session timeout
        if current_time - client_info["last_activity"] > self.session_timeout:
            del self.authenticated_clients[token]
            return False
        
        # Update last activity
        client_info["last_activity"] = current_time
        return True
    
    def process_request(self, request_data, client_socket):
        """Process RPC request with authentication."""
        
        # Check for authentication request
        if request_data.get("method") == "authenticate":
            token = request_data.get("params", {}).get("token")
            timestamp = request_data.get("params", {}).get("timestamp")
            signature = request_data.get("params", {}).get("signature")
            
            success, message = self.authenticate_client(token, timestamp, signature)
            return {"result": {"success": success, "message": message}}
        
        # Check authentication for other requests
        token = request_data.get("auth_token")
        if not token or not self.is_authenticated(token):
            return {"error": "Authentication required"}
        
        # Process authenticated request
        return super().process_request(request_data, client_socket)

class SecureService:
    """Service with role-based access control."""
    
    def __init__(self, server):
        self.server = server
    
    def get_public_data(self):
        """Public method - no special permissions needed."""
        return {"message": "This is public data", "timestamp": time.time()}
    
    def get_user_data(self, user_id):
        """User method - requires authenticated user."""
        return {
            "user_id": user_id,
            "data": f"Private data for user {user_id}",
            "timestamp": time.time()
        }
    
    def admin_operation(self):
        """Admin method - requires admin role."""
        # In real implementation, check user roles
        return {"message": "Admin operation completed", "timestamp": time.time()}

class AuthenticatedRPCClient(RPCClient):
    """RPC client with authentication support."""
    
    def __init__(self, host, port, secret_key):
        super().__init__(host, port)
        self.secret_key = secret_key
        self.auth_token = None
    
    def authenticate(self, username):
        """Authenticate with the server."""
        
        # Generate authentication token
        timestamp = time.time()
        token = f"{username}:{timestamp}"
        
        # Create HMAC signature
        signature = hmac.new(
            self.secret_key.encode(),
            f"{token}:{timestamp}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Send authentication request
        result = self.call("authenticate", {
            "token": token,
            "timestamp": timestamp,
            "signature": signature
        })
        
        if result.get("success"):
            self.auth_token = token
            return True
        else:
            raise Exception(f"Authentication failed: {result.get('message')}")
    
    def call(self, method, *args, **kwargs):
        """Make authenticated RPC call."""
        
        # Add auth token to request if authenticated
        if self.auth_token and method != "authenticate":
            # Override parent's call method to add auth token
            request_data = {
                "method": method,
                "params": {"args": args, "kwargs": kwargs},
                "auth_token": self.auth_token
            }
            return self._send_request(request_data)
        else:
            return super().call(method, *args, **kwargs)

# Usage example
def secure_rpc_example():
    """Example of secure RPC with authentication."""
    
    SECRET_KEY = "your-secret-key-here"
    
    # Start authenticated server
    server = AuthenticatedRPCServer('localhost', 8082, SECRET_KEY)
    secure_service = SecureService(server)
    server.register_service('secure', secure_service)
    
    # Start server in background
    import threading
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    
    # Client usage
    client = AuthenticatedRPCClient('localhost', 8082, SECRET_KEY)
    
    try:
        # Authenticate
        client.authenticate("user123")
        print("Authentication successful")
        
        # Make authenticated calls
        public_data = client.call('secure.get_public_data')
        print(f"Public data: {public_data}")
        
        user_data = client.call('secure.get_user_data', 'user123')
        print(f"User data: {user_data}")
        
        admin_result = client.call('secure.admin_operation')
        print(f"Admin result: {admin_result}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
```

### RPC with Middleware

```python
import time
import logging
from kn_sock import RPCServer

class MiddlewareRPCServer(RPCServer):
    """RPC server with middleware support."""
    
    def __init__(self, host, port):
        super().__init__(host, port)
        self.middleware_stack = []
    
    def add_middleware(self, middleware):
        """Add middleware to the server."""
        self.middleware_stack.append(middleware)
    
    def process_request(self, request_data, client_socket):
        """Process request through middleware stack."""
        
        # Create request context
        context = {
            "request": request_data,
            "client_socket": client_socket,
            "start_time": time.time(),
            "metadata": {}
        }
        
        # Process through middleware (before)
        for middleware in self.middleware_stack:
            if hasattr(middleware, "before_request"):
                middleware.before_request(context)
        
        try:
            # Process the actual request
            result = super().process_request(request_data, client_socket)
            context["result"] = result
            
        except Exception as e:
            context["error"] = e
            raise
        
        finally:
            # Process through middleware (after) - in reverse order
            for middleware in reversed(self.middleware_stack):
                if hasattr(middleware, "after_request"):
                    middleware.after_request(context)
        
        return result

class LoggingMiddleware:
    """Middleware for request/response logging."""
    
    def __init__(self):
        self.logger = logging.getLogger("rpc.requests")
        self.logger.setLevel(logging.INFO)
        
        # Create console handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def before_request(self, context):
        """Log incoming request."""
        request = context["request"]
        client_addr = context["client_socket"].getpeername()
        
        self.logger.info(f"Request from {client_addr}: {request.get('method')} with params {request.get('params')}")
        context["metadata"]["log_id"] = f"{time.time()}_{client_addr[0]}_{client_addr[1]}"
    
    def after_request(self, context):
        """Log request completion."""
        duration = time.time() - context["start_time"]
        log_id = context["metadata"].get("log_id", "unknown")
        
        if "error" in context:
            self.logger.error(f"Request {log_id} failed after {duration:.3f}s: {context['error']}")
        else:
            self.logger.info(f"Request {log_id} completed in {duration:.3f}s")

class RateLimitMiddleware:
    """Middleware for rate limiting."""
    
    def __init__(self, max_requests_per_minute=60):
        self.max_requests = max_requests_per_minute
        self.request_history = {}  # client_ip -> list of timestamps
    
    def before_request(self, context):
        """Check rate limit before processing request."""
        client_ip = context["client_socket"].getpeername()[0]
        current_time = time.time()
        
        # Clean old requests (older than 1 minute)
        if client_ip in self.request_history:
            self.request_history[client_ip] = [
                timestamp for timestamp in self.request_history[client_ip]
                if current_time - timestamp < 60
            ]
        else:
            self.request_history[client_ip] = []
        
        # Check rate limit
        if len(self.request_history[client_ip]) >= self.max_requests:
            raise Exception(f"Rate limit exceeded for {client_ip}")
        
        # Add current request
        self.request_history[client_ip].append(current_time)

class CachingMiddleware:
    """Middleware for response caching."""
    
    def __init__(self, cache_ttl=300):  # 5 minutes default
        self.cache = {}
        self.cache_ttl = cache_ttl
    
    def _get_cache_key(self, request):
        """Generate cache key for request."""
        method = request.get("method")
        params = str(request.get("params", {}))
        return f"{method}:{hash(params)}"
    
    def before_request(self, context):
        """Check cache before processing request."""
        request = context["request"]
        cache_key = self._get_cache_key(request)
        
        if cache_key in self.cache:
            cached_entry = self.cache[cache_key]
            current_time = time.time()
            
            # Check if cache entry is still valid
            if current_time - cached_entry["timestamp"] < self.cache_ttl:
                context["cached_result"] = cached_entry["result"]
                context["cache_hit"] = True
                return
        
        context["cache_key"] = cache_key
        context["cache_hit"] = False
    
    def after_request(self, context):
        """Cache the response after processing."""
        if not context.get("cache_hit") and "result" in context:
            cache_key = context.get("cache_key")
            if cache_key:
                self.cache[cache_key] = {
                    "result": context["result"],
                    "timestamp": time.time()
                }

class MetricsMiddleware:
    """Middleware for collecting metrics."""
    
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_response_time": 0,
            "method_counts": {},
            "response_times": []
        }
    
    def before_request(self, context):
        """Start metrics collection for request."""
        self.metrics["total_requests"] += 1
        method = context["request"].get("method", "unknown")
        
        if method not in self.metrics["method_counts"]:
            self.metrics["method_counts"][method] = 0
        self.metrics["method_counts"][method] += 1
    
    def after_request(self, context):
        """Complete metrics collection for request."""
        duration = time.time() - context["start_time"]
        self.metrics["response_times"].append(duration)
        
        # Keep only last 1000 response times
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"].pop(0)
        
        # Update average response time
        self.metrics["avg_response_time"] = sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
        
        if "error" in context:
            self.metrics["failed_requests"] += 1
        else:
            self.metrics["successful_requests"] += 1
    
    def get_metrics(self):
        """Get current metrics."""
        return self.metrics.copy()

# Usage example
def middleware_rpc_example():
    """Example RPC server with middleware."""
    
    # Create server with middleware
    server = MiddlewareRPCServer('localhost', 8083)
    
    # Add middleware (order matters!)
    server.add_middleware(LoggingMiddleware())
    server.add_middleware(RateLimitMiddleware(max_requests_per_minute=30))
    server.add_middleware(CachingMiddleware(cache_ttl=60))
    metrics_middleware = MetricsMiddleware()
    server.add_middleware(metrics_middleware)
    
    # Register services
    class CalculatorService:
        def add(self, a, b):
            time.sleep(0.1)  # Simulate work
            return a + b
        
        def expensive_calculation(self, n):
            """Expensive operation that benefits from caching."""
            time.sleep(1)  # Simulate expensive calculation
            return sum(range(n))
    
    calc_service = CalculatorService()
    server.register_service('calc', calc_service)
    
    # Register metrics endpoint
    def get_metrics():
        return metrics_middleware.get_metrics()
    
    server.register_function('get_metrics', get_metrics)
    
    print("Middleware RPC Server started on localhost:8083")
    print("Features enabled:")
    print("  - Request/Response logging")
    print("  - Rate limiting (30 requests/minute)")
    print("  - Response caching (60 seconds TTL)")
    print("  - Metrics collection")
    print("\nAvailable methods:")
    print("  - calc.add(a, b)")
    print("  - calc.expensive_calculation(n)")
    print("  - get_metrics()")
    
    server.start()
```

### Load Balanced RPC

```python
import random
import threading
from kn_sock import RPCClient

class LoadBalancedRPCClient:
    """RPC client with load balancing across multiple servers."""
    
    def __init__(self, server_addresses, strategy="round_robin"):
        self.server_addresses = server_addresses
        self.strategy = strategy
        self.clients = {}
        self.current_server = 0
        self.server_health = {}
        
        # Initialize connections
        self.connect_to_servers()
        
        # Start health monitoring
        self.health_monitor_thread = threading.Thread(
            target=self.monitor_server_health, 
            daemon=True
        )
        self.health_monitor_thread.start()
    
    def connect_to_servers(self):
        """Connect to all servers."""
        for address in self.server_addresses:
            try:
                host, port = address.split(':')
                client = RPCClient(host, int(port))
                self.clients[address] = client
                self.server_health[address] = True
                print(f"Connected to {address}")
            except Exception as e:
                print(f"Failed to connect to {address}: {e}")
                self.server_health[address] = False
    
    def get_next_server(self):
        """Get next server based on load balancing strategy."""
        healthy_servers = [addr for addr, healthy in self.server_health.items() if healthy]
        
        if not healthy_servers:
            raise Exception("No healthy servers available")
        
        if self.strategy == "round_robin":
            server = healthy_servers[self.current_server % len(healthy_servers)]
            self.current_server += 1
            return server
        
        elif self.strategy == "random":
            return random.choice(healthy_servers)
        
        elif self.strategy == "least_connections":
            # Simple implementation - could be improved with actual connection counting
            return min(healthy_servers, key=lambda addr: self.get_connection_count(addr))
        
        else:
            return healthy_servers[0]  # Fallback to first healthy server
    
    def get_connection_count(self, address):
        """Get connection count for a server (placeholder implementation)."""
        # In real implementation, track active connections
        return random.randint(1, 10)
    
    def call(self, method, *args, **kwargs):
        """Make load-balanced RPC call."""
        max_retries = len(self.server_addresses)
        
        for attempt in range(max_retries):
            try:
                server_address = self.get_next_server()
                client = self.clients[server_address]
                
                result = client.call(method, *args, **kwargs)
                return result
                
            except Exception as e:
                print(f"Call failed on {server_address}: {e}")
                self.server_health[server_address] = False
                
                if attempt == max_retries - 1:
                    raise Exception(f"All servers failed for method {method}")
    
    def monitor_server_health(self):
        """Monitor server health periodically."""
        import time
        
        while True:
            time.sleep(10)  # Check every 10 seconds
            
            for address in self.server_addresses:
                try:
                    if address in self.clients:
                        # Try a simple health check call
                        self.clients[address].call('health_check')
                        self.server_health[address] = True
                    else:
                        # Try to reconnect
                        host, port = address.split(':')
                        client = RPCClient(host, int(port))
                        self.clients[address] = client
                        self.server_health[address] = True
                        print(f"Reconnected to {address}")
                        
                except Exception:
                    self.server_health[address] = False
    
    def close_all(self):
        """Close all client connections."""
        for client in self.clients.values():
            try:
                client.close()
            except:
                pass

# Service discovery with RPC
class ServiceRegistry:
    """Simple service registry for RPC servers."""
    
    def __init__(self):
        self.services = {}  # service_name -> list of server addresses
        self.server_metadata = {}  # server_address -> metadata
    
    def register_service(self, service_name, server_address, metadata=None):
        """Register a service instance."""
        if service_name not in self.services:
            self.services[service_name] = []
        
        if server_address not in self.services[service_name]:
            self.services[service_name].append(server_address)
            self.server_metadata[server_address] = metadata or {}
            print(f"Registered {service_name} at {server_address}")
        
        return True
    
    def unregister_service(self, service_name, server_address):
        """Unregister a service instance."""
        if service_name in self.services:
            if server_address in self.services[service_name]:
                self.services[service_name].remove(server_address)
                if server_address in self.server_metadata:
                    del self.server_metadata[server_address]
                print(f"Unregistered {service_name} at {server_address}")
                return True
        return False
    
    def discover_service(self, service_name):
        """Discover available instances of a service."""
        return self.services.get(service_name, [])
    
    def list_services(self):
        """List all registered services."""
        return dict(self.services)

# Usage example
def load_balanced_rpc_example():
    """Example of load-balanced RPC."""
    
    # Server addresses (you would start multiple RPC servers)
    server_addresses = [
        'localhost:8080',
        'localhost:8081', 
        'localhost:8082'
    ]
    
    # Create load-balanced client
    lb_client = LoadBalancedRPCClient(server_addresses, strategy="round_robin")
    
    try:
        # Make load-balanced calls
        for i in range(10):
            result = lb_client.call('math.add', i, i * 2)
            print(f"Call {i}: {result}")
        
        # Concurrent calls
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i in range(20):
                future = executor.submit(lb_client.call, 'math.multiply', i, 2)
                futures.append(future)
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                print(f"Concurrent call {i}: {result}")
    
    finally:
        lb_client.close_all()
```

## Protocol Buffers with RPC

```python
# First, install protobuf: pip install protobuf

from kn_sock import RPCServer, RPCClient
import person_pb2  # Generated from person.proto

# person.proto content:
"""
syntax = "proto3";

message Person {
    string name = 1;
    int32 age = 2;
    string email = 3;
    repeated string hobbies = 4;
}

message PersonList {
    repeated Person people = 1;
}
"""

class ProtobufPersonService:
    """RPC service using Protocol Buffers."""
    
    def __init__(self):
        self.people = {}
        self.next_id = 1
    
    def create_person(self, person_data):
        """Create a person from protobuf data."""
        # Deserialize protobuf
        person = person_pb2.Person()
        person.ParseFromString(person_data)
        
        # Store person
        person_id = self.next_id
        self.next_id += 1
        self.people[person_id] = person
        
        return person_id
    
    def get_person(self, person_id):
        """Get a person as protobuf data."""
        if person_id in self.people:
            return self.people[person_id].SerializeToString()
        else:
            raise ValueError(f"Person {person_id} not found")
    
    def list_people(self):
        """Get all people as protobuf data."""
        person_list = person_pb2.PersonList()
        for person in self.people.values():
            person_list.people.append(person)
        
        return person_list.SerializeToString()
    
    def update_person(self, person_id, person_data):
        """Update a person with protobuf data."""
        if person_id not in self.people:
            raise ValueError(f"Person {person_id} not found")
        
        person = person_pb2.Person()
        person.ParseFromString(person_data)
        self.people[person_id] = person
        
        return True

def protobuf_rpc_example():
    """Example using Protocol Buffers with RPC."""
    
    # Start server
    server = RPCServer('localhost', 8084)
    person_service = ProtobufPersonService()
    server.register_service('person', person_service)
    
    # Start server in background
    import threading
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    
    # Client usage
    client = RPCClient('localhost', 8084)
    
    try:
        # Create person using protobuf
        person = person_pb2.Person()
        person.name = "Alice Johnson"
        person.age = 30
        person.email = "alice@example.com"
        person.hobbies.extend(["reading", "hiking", "photography"])
        
        # Serialize and send
        person_data = person.SerializeToString()
        person_id = client.call('person.create_person', person_data)
        print(f"Created person with ID: {person_id}")
        
        # Retrieve person
        retrieved_data = client.call('person.get_person', person_id)
        
        # Deserialize
        retrieved_person = person_pb2.Person()
        retrieved_person.ParseFromString(retrieved_data)
        
        print(f"Retrieved person: {retrieved_person.name}, age {retrieved_person.age}")
        print(f"Email: {retrieved_person.email}")
        print(f"Hobbies: {list(retrieved_person.hobbies)}")
        
        # Create more people
        for i in range(3):
            person = person_pb2.Person()
            person.name = f"Person {i+2}"
            person.age = 25 + i
            person.email = f"person{i+2}@example.com"
            person.hobbies.extend([f"hobby{i+1}", f"hobby{i+2}"])
            
            person_data = person.SerializeToString()
            client.call('person.create_person', person_data)
        
        # List all people
        people_data = client.call('person.list_people')
        people_list = person_pb2.PersonList()
        people_list.ParseFromString(people_data)
        
        print(f"\nAll people ({len(people_list.people)}):")
        for person in people_list.people:
            print(f"  - {person.name}, age {person.age}")
    
    finally:
        client.close()
```

## Performance Monitoring

```python
import time
import threading
import statistics
from collections import defaultdict, deque

class PerformanceMonitor:
    """Performance monitoring for RPC servers."""
    
    def __init__(self, window_size=1000):
        self.window_size = window_size
        self.call_times = deque(maxlen=window_size)
        self.method_stats = defaultdict(lambda: {
            "count": 0,
            "total_time": 0,
            "times": deque(maxlen=100)
        })
        self.error_count = 0
        self.start_time = time.time()
    
    def record_call(self, method, duration, success=True):
        """Record an RPC call."""
        self.call_times.append(duration)
        
        stats = self.method_stats[method]
        stats["count"] += 1
        stats["total_time"] += duration
        stats["times"].append(duration)
        
        if not success:
            self.error_count += 1
    
    def get_stats(self):
        """Get current performance statistics."""
        if not self.call_times:
            return {"error": "No data available"}
        
        total_calls = len(self.call_times)
        avg_time = statistics.mean(self.call_times)
        median_time = statistics.median(self.call_times)
        
        stats = {
            "uptime": time.time() - self.start_time,
            "total_calls": total_calls,
            "error_count": self.error_count,
            "error_rate": self.error_count / total_calls if total_calls > 0 else 0,
            "avg_call_time": avg_time,
            "median_call_time": median_time,
            "calls_per_second": total_calls / (time.time() - self.start_time),
            "method_stats": {}
        }
        
        # Add per-method statistics
        for method, method_stats in self.method_stats.items():
            if method_stats["times"]:
                stats["method_stats"][method] = {
                    "count": method_stats["count"],
                    "avg_time": method_stats["total_time"] / method_stats["count"],
                    "median_time": statistics.median(method_stats["times"]),
                    "min_time": min(method_stats["times"]),
                    "max_time": max(method_stats["times"])
                }
        
        return stats

class MonitoredRPCServer(RPCServer):
    """RPC server with built-in performance monitoring."""
    
    def __init__(self, host, port):
        super().__init__(host, port)
        self.monitor = PerformanceMonitor()
    
    def process_request(self, request_data, client_socket):
        """Process request with performance monitoring."""
        method = request_data.get("method", "unknown")
        start_time = time.time()
        success = True
        
        try:
            result = super().process_request(request_data, client_socket)
            return result
        except Exception as e:
            success = False
            raise
        finally:
            duration = time.time() - start_time
            self.monitor.record_call(method, duration, success)
    
    def get_performance_stats(self):
        """Get performance statistics."""
        return self.monitor.get_stats()

# Register performance endpoint
def setup_monitored_server():
    """Set up RPC server with monitoring."""
    
    server = MonitoredRPCServer('localhost', 8085)
    
    # Register the stats endpoint
    server.register_function('get_stats', server.get_performance_stats)
    
    # Add some example services
    class BenchmarkService:
        def fast_operation(self):
            return "fast"
        
        def slow_operation(self):
            time.sleep(0.5)
            return "slow"
        
        def error_operation(self):
            raise ValueError("Intentional error for testing")
    
    benchmark_service = BenchmarkService()
    server.register_service('benchmark', benchmark_service)
    
    return server

# Usage
if __name__ == "__main__":
    server = setup_monitored_server()
    
    print("Monitored RPC Server started on localhost:8085")
    print("Performance monitoring enabled")
    print("Available methods:")
    print("  - benchmark.fast_operation()")
    print("  - benchmark.slow_operation()")
    print("  - benchmark.error_operation()")
    print("  - get_stats()")
    
    server.start()
```

## See Also

- **[TCP Protocol](../protocols/tcp.md)** - For reliable RPC transport
- **[JSON Communication](../protocols/json.md)** - For JSON-based RPC
- **[Pub/Sub Messaging](pubsub.md)** - For event-driven communication
- **[WebSocket Protocol](../protocols/websocket.md)** - For real-time RPC
- **[Examples](../examples.md)** - RPC application examples
