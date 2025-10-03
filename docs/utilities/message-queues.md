# Message Queues

Thread-safe message queues for buffering and processing messages.

## Classes

### `InMemoryQueue`
Thread-safe in-memory FIFO queue.

**Methods:**
- `put(item)` - Add item to queue
- `get(block=True, timeout=None)` - Get item from queue
- `task_done()` - Mark task as complete
- `join()` - Wait until all tasks are done
- `qsize()` - Return queue size
- `empty()` - Return True if queue is empty

**Example:**
```python
from kn_sock.queue import InMemoryQueue
import threading

queue = InMemoryQueue()

# Producer thread
def producer():
    for i in range(5):
        queue.put(f"message-{i}")
        
# Consumer thread  
def consumer():
    while True:
        item = queue.get()
        print(f"Processing: {item}")
        queue.task_done()

threading.Thread(target=producer).start()
threading.Thread(target=consumer, daemon=True).start()
queue.join()  # Wait for all tasks to complete
```

### `FileQueue(path)`
Persistent file-based queue that survives restarts.

**Parameters:**
- `path` (str): File path for queue storage

**Methods:**
- `put(item)` - Add item to queue (saves to disk)
- `get(block=True, timeout=None)` - Get item from queue
- `task_done()` - Mark task as complete
- `join()` - Wait until all tasks are done
- `close()` - Save queue state and close
- `qsize()` - Return queue size
- `empty()` - Return True if queue is empty

**Example:**
```python
from kn_sock.queue import FileQueue

# Create persistent queue
queue = FileQueue("messages.db")

# Add messages
queue.put("message 1")
queue.put("message 2")

# Process messages
try:
    while not queue.empty():
        item = queue.get(timeout=1)
        print(f"Processing: {item}")
        queue.task_done()
except:
    pass

queue.close()  # Save state
```

## Usage with Socket Servers

```python
from kn_sock import start_tcp_server
from kn_sock.queue import InMemoryQueue
import threading

message_queue = InMemoryQueue()

def message_handler(data, addr, socket):
    # Add incoming messages to queue
    message_queue.put((data, addr, socket))

def message_processor():
    # Process messages from queue
    while True:
        data, addr, socket = message_queue.get()
        
        # Process the message
        response = f"Processed: {data.decode()}"
        socket.sendall(response.encode())
        
        message_queue.task_done()

# Start background processor
threading.Thread(target=message_processor, daemon=True).start()

# Start server
start_tcp_server(8080, message_handler)
```
