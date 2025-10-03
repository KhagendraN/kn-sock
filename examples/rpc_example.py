#!/usr/bin/env python3
"""
Complete RPC Working Example - From Documentation

This example demonstrates the correct kn-sock RPC API usage.
Copy this example and it should work immediately.
"""

from kn_sock import start_rpc_server, RPCClient
import threading
import time

def start_math_rpc_server():
    """Start a basic RPC server - matches documentation."""
    
    class MathService:
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

def test_rpc_client():
    """Example RPC client - matches documentation."""
    
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

def main():
    print("=" * 50)
    print("kn-sock RPC Documentation Example")
    print("=" * 50)
    
    # Start server in background
    server_thread = threading.Thread(target=start_math_rpc_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Test client
    test_rpc_client()

if __name__ == "__main__":
    main()
