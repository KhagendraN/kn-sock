# Queue Utilities

kn-sock includes basic queue utilities and configuration helpers—useful for message buffering, distributed jobs, and customizing runtime behavior.

## CLI Commands

_No dedicated CLI commands for queues or config. Use Python API as shown below._

## Python API

### In-Memory Queue Example

Use the built-in `Queue` for simple producer/consumer patterns.

```python
from kn_sock.queue import Queue

q = Queue()
q.put("job1")
q.put("job2")

while not q.empty():
    print(q.get())
# Output:
# job1
# job2
```

### Configuration Example

Configuration options can be set using environment variables or passed directly to API calls.  
Most CLI commands also accept `--host`, `--port`, or other options for customization.

## Sample Output
```
job1
job2
```

## Known Issues & Troubleshooting
| Issue             | Symptom/Output       | Solution                              |
|-------------------|---------------------|---------------------------------------|
| Queue deadlock    | Script hangs        | Use timeouts or check `empty()` before `get()` |
| Invalid config    | Errors at runtime   | Check supported options in the docs   |

## Testing
### Manual Test
Create a Python script:
```python
from kn_sock.queue import Queue
q = Queue()
q.put("test1")
q.put("test2")
while not q.empty():
    print(q.get())
```

Run the script. You should see both items printed.