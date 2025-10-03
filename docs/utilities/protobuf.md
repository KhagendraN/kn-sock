# Protocol Buffers

Protocol Buffers (protobuf) serialization utilities.

**Requirement:** `pip install protobuf`

## Functions

### `serialize_message(msg)`
Serialize a protobuf message to bytes.

**Parameters:**
- `msg` - Protobuf message instance

**Returns:** bytes - Serialized data

### `deserialize_message(data, schema)`
Deserialize bytes to a protobuf message.

**Parameters:**
- `data` (bytes): Serialized protobuf data
- `schema` (Type): Protobuf message class

**Returns:** Protobuf message instance

## Usage Example

```python
# First, create your protobuf definition (example.proto):
# syntax = "proto3";
# message Person {
#   string name = 1;
#   int32 age = 2;
# }

# Generate Python classes: protoc --python_out=. example.proto

from kn_sock.protobuf import serialize_message, deserialize_message
from example_pb2 import Person

# Create and serialize message
person = Person(name="Alice", age=30)
data = serialize_message(person)

# Send over network
send_tcp_message("localhost", 8080, data)

# Deserialize received data
def handler(data, addr, socket):
    person = deserialize_message(data, Person)
    print(f"Received: {person.name}, age {person.age}")
```

## Integration with kn-sock

```python
from kn_sock import start_tcp_server, send_tcp_message
from kn_sock.protobuf import serialize_message, deserialize_message
from my_messages_pb2 import RequestMessage, ResponseMessage

def protobuf_handler(data, addr, socket):
    # Deserialize request
    request = deserialize_message(data, RequestMessage)
    
    # Process request
    response = ResponseMessage(
        id=request.id,
        result="Success"
    )
    
    # Send serialized response
    response_data = serialize_message(response)
    socket.sendall(response_data)

start_tcp_server(8080, protobuf_handler)
```
