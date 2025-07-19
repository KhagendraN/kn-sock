"""
Test Utilities Example

Demonstrates using kn-sock's CLI and utility functions for network testing.

How to run:
    # Get a free port
    python test_utilities.py free_port

    # Get local IP
    python test_utilities.py local_ip
"""
import sys
from kn_sock import get_free_port, get_local_ip


def free_port():
    port = get_free_port()
    print("Free port:", port)


def local_ip():
    ip = get_local_ip()
    print("Local IP:", ip)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_utilities.py [free_port|local_ip]")
        sys.exit(1)
    if sys.argv[1] == "free_port":
        free_port()
    elif sys.argv[1] == "local_ip":
        local_ip()
    else:
        print("Unknown command.")
