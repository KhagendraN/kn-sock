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
## See Also

- **[TCP Protocol](../protocols/tcp.md)** - For reliable RPC transport
- **[JSON Communication](../protocols/json.md)** - For structured RPC data
- **[PubSub Messaging](pubsub.md)** - For event-driven communication
- **[WebSocket Protocol](../protocols/websocket.md)** - For real-time RPC
- **[Examples](../examples.md)** - More RPC application examples
