"""
kn_sock.protobuf

Utilities for protocol buffers (protobuf) serialization and deserialization.

Usage:
    from kn_sock.protobuf import serialize_message, deserialize_message
    from my_proto_pb2 import MyMessage
    msg = MyMessage(field1='abc', field2=123)
    data = serialize_message(msg)
    restored = deserialize_message(data, MyMessage)

Requires: pip install protobuf
"""
from typing import Type


def serialize_message(msg) -> bytes:
    """Serialize a protobuf message to bytes."""
    return msg.SerializeToString()


def deserialize_message(data: bytes, schema: Type) -> object:
    """Deserialize bytes to a protobuf message (given the schema class)."""
    msg = schema()
    msg.ParseFromString(data)
    return msg 