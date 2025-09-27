# Remote Procedure Calls (RPC)

kn-sock provides a simple and efficient JSON-RPC system that allows you to call functions on remote servers as if they were local.

## Overview

RPC features in kn-sock:
- **JSON-RPC protocol**: Standard JSON-RPC over TCP
- **Synchronous calls**: Simple request-response pattern
- **Error handling**: Automatic exception propagation across network
- **Multi-threaded server**: Handles multiple clients concurrently
- **Simple API**: Easy-to-use function-based interface

## Basic RPC Usage

### RPC Server

```python
from kn_sock import start_rpc_server

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

def start_math_rpc_server():
    """Start a basic RPC server."""
    
    # Create service instance
    math_service = MathService()
    
    # Define additional functions
    def hello(name):
        return f"Hello, {name}!"
    
    def get_server_time():
        import datetime
        return datetime.datetime.now().isoformat()
    
    # Register all functions in a flat dictionary
    register_funcs = {
        # Math service methods
        'add': math_service.add,
        'subtract': math_service.subtract,
        'multiply': math_service.multiply,
        'divide': math_service.divide,
        'factorial': math_service.factorial,
        
        # Standalone functions  
        'hello': hello,
        'get_time': get_server_time
    }
    
    print("🚀 Starting RPC Server on localhost:8080")
    print("📋 Available RPC methods:")
    for method_name in register_funcs.keys():
        print(f"  - {method_name}")
    
    # Start the RPC server
    start_rpc_server(
        port=8080,
        register_funcs=register_funcs,
        host='0.0.0.0'
    )

if __name__ == "__main__":
    start_math_rpc_server()
```

### RPC Client

```python
from kn_sock import RPCClient

def test_rpc_client():
    """Example RPC client."""
    
    client = None
    try:
        # Connect to RPC server
        client = RPCClient('localhost', 8080)
        print("✅ Connected to RPC server")
        
        # Call individual functions
        greeting = client.call('hello', 'Alice')
        print(f"Greeting: {greeting}")
        
        server_time = client.call('get_time')
        print(f"Server time: {server_time}")
        
        # Call math functions
        result = client.call('add', 10, 20)
        print(f"10 + 20 = {result}")
        
        result = client.call('multiply', 7, 8)
        print(f"7 * 8 = {result}")
        
        result = client.call('factorial', 5)
        print(f"5! = {result}")
        
        # Handle errors
        try:
            result = client.call('divide', 10, 0)
            print(f"10 / 0 = {result}")
        except Exception as e:
            print(f"Division by zero error: {e}")
        
        # Call non-existent method
        try:
            result = client.call('non_existent_method')
        except Exception as e:
            print(f"Method not found error: {e}")
        
    except ConnectionRefusedError:
        print("❌ Could not connect to RPC server. Is it running?")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if client is not None:
            client.close()
            print("🔒 Client connection closed")

if __name__ == "__main__":
    test_rpc_client()
```

## Multi-Service RPC Example

kn-sock RPC supports registering multiple services and utility functions on a single server. Here's a comprehensive example:

### Complete RPC Server with Multiple Services

```python
#!/usr/bin/env python3
"""
Complete RPC Example - Server and Client
"""

from kn_sock import start_rpc_server, RPCClient
import threading
import time

# Service classes
class CalculatorService:
    """Calculator service with basic math operations."""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

class UserService:
    """User service with user management operations."""
    
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def create_user(self, name, email):
        user_id = self.next_id
        self.next_id += 1
        self.users[user_id] = {
            'id': user_id,
            'name': name,
            'email': email,
            'created_at': time.time()
        }
        return self.users[user_id]
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def list_users(self):
        return list(self.users.values())
    
    def delete_user(self, user_id):
        return self.users.pop(user_id, None)

def start_demo_rpc_server():
    """Start RPC server with multiple services."""
    
    # Create service instances
    calc = CalculatorService()
    user_service = UserService()
    
    # Utility functions
    def ping():
        return "pong"
    
    def get_server_info():
        import platform
        return {
            "server": "kn-sock RPC Demo",
            "python_version": platform.python_version(),
            "platform": platform.system(),
            "timestamp": time.time()
        }
    
    # Register all functions
    register_funcs = {
        # Calculator service
        'calc_add': calc.add,
        'calc_subtract': calc.subtract,
        'calc_multiply': calc.multiply,
        'calc_divide': calc.divide,
        
        # User service
        'user_create': user_service.create_user,
        'user_get': user_service.get_user,
        'user_list': user_service.list_users,
        'user_delete': user_service.delete_user,
        
        # Utility functions
        'ping': ping,
        'server_info': get_server_info
    }
    
    print("🚀 Starting RPC Demo Server on port 8080")
    print("📋 Available RPC methods:")
    for method in sorted(register_funcs.keys()):
        print(f"  - {method}")
    print()
    
    # Start server
    start_rpc_server(
        port=8080,
        register_funcs=register_funcs,
        host='0.0.0.0'
    )

def demo_rpc_client():
    """Demo RPC client showing various operations."""
    
    client = None
    try:
        client = RPCClient("localhost", 8080)
        print("✅ Connected to RPC server\n")
        
        # Test basic functions
        print("🏓 Testing ping:")
        response = client.call("ping")
        print(f"  ping() = {response}\n")
        
        # Test server info
        print("ℹ️  Getting server info:")
        info = client.call("server_info")
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()
        
        # Test calculator
        print("🧮 Testing Calculator Service:")
        print(f"  calc_add(15, 7) = {client.call('calc_add', 15, 7)}")
        print(f"  calc_multiply(8, 9) = {client.call('calc_multiply', 8, 9)}")
        print(f"  calc_divide(100, 4) = {client.call('calc_divide', 100, 4)}")
        print()
        
        # Test user service
        print("👥 Testing User Service:")
        
        # Create users
        user1 = client.call("user_create", "Alice Smith", "alice@example.com")
        user2 = client.call("user_create", "Bob Johnson", "bob@example.com")
        print(f"  Created user: {user1}")
        print(f"  Created user: {user2}")
        
        # Get user
        retrieved_user = client.call("user_get", user1['id'])
        print(f"  Retrieved user {user1['id']}: {retrieved_user}")
        
        # List users
        all_users = client.call("user_list")
        print(f"  All users: {len(all_users)} users")
        
        # Delete user
        deleted_user = client.call("user_delete", user2['id'])
        print(f"  Deleted user: {deleted_user}")
        print()
        
        # Test error handling
        print("❌ Testing Error Handling:")
        try:
            result = client.call("calc_divide", 10, 0)
        except Exception as e:
            print(f"  Division by zero: {e}")
        
        try:
            result = client.call("non_existent_method")
        except Exception as e:
            print(f"  Non-existent method: {e}")
        
        print("\n✅ All RPC demo operations completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if client is not None:
            client.close()
            print("🔒 Client disconnected")

def main():
    """Run the complete RPC demo."""
    print("=" * 60)
    print("kn-sock RPC Complete Demo")
    print("=" * 60)
    
    # Start server in background
    server_thread = threading.Thread(target=start_demo_rpc_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Run client demo
    demo_rpc_client()

if __name__ == "__main__":
    main()
```

## Message Protocol

RPC uses JSON-RPC over TCP with newline-delimited messages:

### Request Format
```json
{
  "method": "function_name",
  "params": [arg1, arg2, ...],
  "kwargs": {"key": "value"}
}
```

### Response Format (Success)
```json
{
  "result": "return_value"
}
```

### Response Format (Error)
```json
{
  "error": "error_message"
}
```

## Advanced RPC Patterns

### Function Organization

Organize your RPC functions logically with prefixes:

```python
from kn_sock import start_rpc_server

class UserService:
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def create(self, name, email):
        user_id = self.next_id
        self.next_id += 1
        self.users[user_id] = {"id": user_id, "name": name, "email": email}
        return self.users[user_id]
    
    def get(self, user_id):
        return self.users.get(user_id)
    
    def list_all(self):
        return list(self.users.values())

class AuthService:
    def __init__(self):
        self.sessions = {}
    
    def login(self, username, password):
        # Simple authentication (use proper auth in production)
        if username == "admin" and password == "secret":
            session_id = f"session_{len(self.sessions) + 1}"
            self.sessions[session_id] = {"username": username}
            return {"session_id": session_id, "username": username}
        else:
            raise ValueError("Invalid credentials")
    
    def logout(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def validate(self, session_id):
        return self.sessions.get(session_id)

# Good: Use prefixes to group related functions
def start_organized_rpc_server():
    user_service = UserService()
    auth_service = AuthService()
    
    register_funcs = {
        # User service functions
        'user_create': user_service.create,
        'user_get': user_service.get,
        'user_list': user_service.list_all,
        
        # Auth service functions
        'auth_login': auth_service.login,
        'auth_logout': auth_service.logout,
        'auth_validate': auth_service.validate,
        
        # Utility functions
        'ping': lambda: "pong",
        'server_info': lambda: {"server": "organized-rpc", "version": "1.0"}
    }
    
    start_rpc_server(8080, register_funcs)
```

### Parameter Validation

Always validate parameters in your RPC functions:

```python
def divide(a, b):
    # Validate parameter types
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Parameters must be numbers")
    
    # Validate parameter values
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    
    return a / b

def create_user(name, email, age=None):
    # Validate required parameters
    if not name or not isinstance(name, str):
        raise ValueError("Name must be a non-empty string")
    
    if not email or "@" not in email:
        raise ValueError("Valid email address required")
    
    # Validate optional parameters
    if age is not None and (not isinstance(age, int) or age < 0):
        raise ValueError("Age must be a positive integer")
    
    return {"name": name, "email": email, "age": age}
```

### Error Handling Best Practices

Always wrap RPC calls in try-except blocks:

```python
from kn_sock import RPCClient

def safe_rpc_call():
    """Example of proper RPC client error handling."""
    client = None
    try:
        client = RPCClient("localhost", 8080)
        result = client.call("some_method", arg1, arg2)
        return result
    except ConnectionRefusedError:
        print("❌ RPC server is not running")
        return None
    except Exception as e:
        print(f"❌ RPC error: {e}")
        return None
    finally:
        if client:
            client.close()

# Better: Use a context manager pattern
class RPCContextClient:
    """Context manager for RPC client connections."""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
    
    def __enter__(self):
        self.client = RPCClient(self.host, self.port)
        return self.client
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

# Usage with context manager
def example_with_context_manager():
    try:
        with RPCContextClient("localhost", 8080) as rpc:
            result = rpc.call("ping")
            print(f"Ping result: {result}")
            
            user = rpc.call("user_create", "Alice", "alice@example.com")
            print(f"Created user: {user}")
            
    except Exception as e:
        print(f"RPC error: {e}")
```

### Microservices Communication

Use RPC to connect different services in a microservices architecture:

```python
from kn_sock import start_rpc_server, RPCClient
import threading
import time

# User Service (Port 8080)
def start_user_service():
    """Independent user management service."""
    
    class UserService:
        def __init__(self):
            self.users = {}
            self.next_id = 1
        
        def create_user(self, name, email):
            user_id = self.next_id
            self.next_id += 1
            user = {
                'id': user_id,
                'name': name,
                'email': email,
                'created_at': time.time()
            }
            self.users[user_id] = user
            return user
        
        def get_user(self, user_id):
            return self.users.get(user_id)
        
        def list_users(self):
            return list(self.users.values())
    
    service = UserService()
    start_rpc_server(8080, {
        'create_user': service.create_user,
        'get_user': service.get_user,
        'list_users': service.list_users
    })

# Order Service (Port 8081) - calls User Service
def start_order_service():
    """Order service that depends on user service."""
    
    class OrderService:
        def __init__(self):
            self.orders = {}
            self.next_id = 1
        
        def create_order(self, user_id, items, total):
            # Verify user exists by calling user service
            user_client = RPCClient("localhost", 8080)
            try:
                user = user_client.call("get_user", user_id)
                if not user:
                    raise ValueError("User not found")
                
                # Create order
                order_id = self.next_id
                self.next_id += 1
                order = {
                    'id': order_id,
                    'user_id': user_id,
                    'user_name': user['name'],
                    'items': items,
                    'total': total,
                    'created_at': time.time()
                }
                self.orders[order_id] = order
                return order
                
            finally:
                user_client.close()
        
        def get_order(self, order_id):
            return self.orders.get(order_id)
        
        def list_orders_by_user(self, user_id):
            return [order for order in self.orders.values() 
                   if order['user_id'] == user_id]
    
    service = OrderService()
    start_rpc_server(8081, {
        'create_order': service.create_order,
        'get_order': service.get_order,
        'list_orders_by_user': service.list_orders_by_user
    })

# Example: Start microservices
def start_microservices_demo():
    """Start microservices in background threads."""
    
    print("Starting User Service on port 8080...")
    user_thread = threading.Thread(target=start_user_service, daemon=True)
    user_thread.start()
    time.sleep(1)
    
    print("Starting Order Service on port 8081...")
    order_thread = threading.Thread(target=start_order_service, daemon=True)
    order_thread.start()
    time.sleep(1)
    
    print("Services started!")
    
    # Test the services
    print("\nTesting microservices...")
    
    # Create a user
    user_client = RPCClient("localhost", 8080)
    try:
        user = user_client.call("create_user", "Alice", "alice@example.com")
        print(f"Created user: {user}")
    finally:
        user_client.close()
    
    # Create an order
    order_client = RPCClient("localhost", 8081)
    try:
        order = order_client.call("create_order", user['id'], ["item1", "item2"], 29.99)
        print(f"Created order: {order}")
    finally:
        order_client.close()

if __name__ == "__main__":
    start_microservices_demo()
    # Keep main alive
    while True:
        time.sleep(1)
```

## CLI Usage

You can test RPC functionality from the command line:

```bash
# Start your RPC server
python my_rpc_server.py

# Test with netcat (basic JSON-RPC)
echo '{"method": "ping", "params": []}' | nc localhost 8080

# Test with curl (if using HTTP wrapper)
curl -X POST http://localhost:8080 -d '{"method": "ping", "params": []}'
```

## Testing RPC Services

Example unit tests for RPC services:

```python
import unittest
import threading
import time
from kn_sock import start_rpc_server, RPCClient

class TestRPCService(unittest.TestCase):
    """Test RPC service functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Start RPC server for testing."""
        
        def add(a, b):
            return a + b
        
        def divide(a, b):
            if b == 0:
                raise ValueError("Division by zero")
            return a / b
        
        cls.register_funcs = {
            'add': add,
            'divide': divide,
            'ping': lambda: "pong"
        }
        
        # Start server in background
        cls.server_thread = threading.Thread(
            target=lambda: start_rpc_server(8087, cls.register_funcs),
            daemon=True
        )
        cls.server_thread.start()
        time.sleep(1)  # Wait for server to start
    
    def setUp(self):
        """Create RPC client for each test."""
        self.client = RPCClient("localhost", 8087)
    
    def tearDown(self):
        """Clean up RPC client."""
        self.client.close()
    
    def test_ping(self):
        """Test basic connectivity."""
        result = self.client.call("ping")
        self.assertEqual(result, "pong")
    
    def test_add(self):
        """Test addition function."""
        result = self.client.call("add", 5, 3)
        self.assertEqual(result, 8)
    
    def test_divide_success(self):
        """Test successful division."""
        result = self.client.call("divide", 10, 2)
        self.assertEqual(result, 5.0)
    
    def test_divide_by_zero(self):
        """Test division by zero error handling."""
        with self.assertRaises(Exception):
            self.client.call("divide", 10, 0)
    
    def test_nonexistent_method(self):
        """Test calling non-existent method."""
        with self.assertRaises(Exception):
            self.client.call("nonexistent_method")

if __name__ == "__main__":
    unittest.main()
```

## Troubleshooting

### Common Issues

**Connection Refused:**
- Check if the RPC server is running
- Verify the correct host and port
- Check firewall settings
- Verify the server has started successfully

**JSON Decode Errors:**
- Ensure parameters are JSON-serializable
- Check for circular references in objects
- Use simple data types (int, float, str, list, dict)

**Method Not Found:**
- Verify the method name is registered correctly
- Check spelling and case sensitivity
- Ensure the function is in the register_funcs dictionary

**Timeout Issues:**
- Server may be overloaded with requests
- Network connectivity problems
- Long-running functions blocking the server thread
- Consider breaking up long operations

### Performance Tips

- **Keep RPC functions lightweight**: Avoid long-running operations that block the server
- **Use connection pooling**: For frequent calls to the same server
- **Consider batching**: Group multiple calls when possible
- **Monitor resources**: Watch server CPU and memory usage
- **Validate early**: Check parameters at the start of functions
- **Use threading wisely**: The server handles multiple clients via threading

### Security Considerations

```python
def secure_function(api_key, user_id):
    """Example of basic API key validation."""
    VALID_API_KEY = "your-secret-key"
    
    # Validate API key
    if api_key != VALID_API_KEY:
        raise ValueError("Invalid API key")
    
    # Validate user_id format
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID")
    
    # Your secure logic here
    return {"user_id": user_id, "data": "sensitive information"}

# Register with validation
register_funcs = {
    'secure_function': secure_function
}
```

## Async RPC Alternative

While kn-sock doesn't have built-in async RPC, you can implement async RPC patterns using the available async TCP functionality:

```python
import asyncio
import json
from kn_sock import start_async_tcp_server, send_tcp_message_async

class AsyncRPCHandler:
    """Custom async RPC handler using async TCP."""
    
    def __init__(self):
        self.functions = {}
        self.data = {}  # Example data store
    
    def register(self, name, func):
        """Register an async function."""
        self.functions[name] = func
    
    async def handle_request(self, data, addr, transport):
        """Handle incoming RPC requests."""
        try:
            # Parse JSON-RPC request
            request = json.loads(data.decode())
            method = request.get("method")
            params = request.get("params", [])
            
            if method not in self.functions:
                response = {"error": f"Method '{method}' not found"}
            else:
                # Call the async function
                try:
                    result = await self.functions[method](*params)
                    response = {"result": result}
                except Exception as e:
                    response = {"error": str(e)}
            
            # Send response back
            response_data = json.dumps(response).encode() + b"\n"
            transport.sendto(response_data, addr)
            
        except json.JSONDecodeError:
            error_response = {"error": "Invalid JSON"}
            transport.sendto(json.dumps(error_response).encode() + b"\n", addr)
        except Exception as e:
            error_response = {"error": f"Server error: {str(e)}"}
            transport.sendto(json.dumps(error_response).encode() + b"\n", addr)

# Example async RPC server
async def start_custom_async_rpc():
    """Start custom async RPC server."""
    
    handler = AsyncRPCHandler()
    
    # Register async functions
    async def async_add(a, b):
        await asyncio.sleep(0.1)  # Simulate async work
        return a + b
    
    async def async_get_data(key):
        await asyncio.sleep(0.05)  # Simulate database lookup
        return handler.data.get(key, "Not found")
    
    async def async_set_data(key, value):
        await asyncio.sleep(0.05)  # Simulate database write
        handler.data[key] = value
        return True
    
    handler.register("add", async_add)
    handler.register("get", async_get_data)  
    handler.register("set", async_set_data)
    
    print("🚀 Starting custom async RPC server on UDP port 8088")
    
    # Start the async server
    shutdown_event = asyncio.Event()
    await start_udp_server_async(8088, handler.handle_request, shutdown_event)

# Note: This is a custom implementation for demonstration
# The standard kn-sock RPC uses start_rpc_server which is synchronous but multi-threaded
```

## See Also

- **[TCP Protocol](../protocols/tcp.md)** - For reliable RPC transport
- **[JSON Communication](../protocols/json.md)** - For structured RPC data
- **[PubSub Messaging](pubsub.md)** - For event-driven communication
- **[WebSocket Protocol](../protocols/websocket.md)** - For real-time RPC
- **[Examples](../examples.md)** - More RPC application examples
