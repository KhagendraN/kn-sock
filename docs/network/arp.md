# ARP Scanning

ARP (Address Resolution Protocol) scanning allows you to discover active devices on your local network by sending ARP requests and analyzing responses.

⚠️ **ETHICAL WARNING**: ARP scanning is intended for use in authorized networks only. This tool should only be used in controlled IT environments, schools, or labs with proper authorization. Unauthorized network scanning may be illegal and unethical.

## Features

- **Network Discovery**: Find all active devices on a subnet
- **MAC Address Resolution**: Get MAC addresses for discovered devices
- **Interface Auto-Detection**: Automatically detect the best network interface
- **Customizable Timeouts**: Adjust scan speed and reliability
- **Verbose Logging**: Detailed output for troubleshooting

## Installation

ARP scanning requires the `scapy` library:

```bash
pip install scapy
```

For complete dependency information, see the [API Reference](api-reference.md#dependencies).

## Basic Usage

### Python API

```python
from kn_sock.network import arp_scan

# Scan a local network
devices = arp_scan("192.168.1.0/24")
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}")
```

### Command Line

```bash
# Basic scan
knsock scan 192.168.1.0/24

# Verbose output
knsock scan 192.168.1.0/24 --verbose

# Custom interface and timeout
knsock scan 192.168.1.0/24 --interface eth0 --timeout 5
```

For complete CLI documentation, see the [API Reference](api-reference.md#cli-commands).

## Advanced Usage

### Custom Interface Selection

```python
from kn_sock.network import arp_scan

# Specify network interface
devices = arp_scan("192.168.1.0/24", interface="eth0")
```

### Verbose Logging

```python
from kn_sock.network import arp_scan

# Enable detailed logging
devices = arp_scan("192.168.1.0/24", verbose=True)
```

### Simple IP/MAC Pairs

```python
from kn_sock.network.arp import arp_scan_simple

# Get simple (IP, MAC) tuples
device_pairs = arp_scan_simple("192.168.1.0/24")
for ip, mac in device_pairs:
    print(f"{ip} -> {mac}")
```

### Network Information

```python
from kn_sock.network.arp import get_local_network_info

# Get local network details
info = get_local_network_info()
print(f"Local IP: {info['local_ip']}")
print(f"Interface: {info['interface']}")
print(f"Gateway: {info['gateway']}")
```

## Function Reference

For complete API documentation, see the [API Reference](api-reference.md#arp-scanning-functions).

## Common Network Ranges

| Range | Description | Example |
|-------|-------------|---------|
| `/24` | 256 addresses | 192.168.1.0/24 |
| `/16` | 65,536 addresses | 192.168.0.0/16 |
| `/8` | 16,777,216 addresses | 10.0.0.0/8 |

## Troubleshooting

### Permission Issues

ARP scanning requires network access. On Linux/macOS, you may need to run with elevated privileges:

```bash
sudo knsock scan 192.168.1.0/24
```

### No Devices Found

1. **Check Network Range**: Ensure you're scanning the correct subnet
2. **Verify Interface**: Use `--interface` to specify the correct network interface
3. **Firewall**: Some devices may not respond to ARP requests due to firewall settings
4. **Network Isolation**: Ensure you're on the same network segment

### Interface Detection

List available interfaces:

```python
from kn_sock.network.monitor import get_network_interfaces

interfaces = get_network_interfaces()
for iface in interfaces:
    print(f"{iface['name']}: {iface['ip']}")
```

### Timeout Issues

Increase timeout for slower networks:

```python
devices = arp_scan("192.168.1.0/24", timeout=5)
```

## Security Considerations

1. **Authorization**: Only scan networks you own or have permission to monitor
2. **Legal Compliance**: Ensure compliance with local network monitoring laws
3. **Network Impact**: ARP scanning generates network traffic - use responsibly
4. **Detection**: Some network monitoring tools may detect ARP scans

For complete security and legal information, see the [API Reference](api-reference.md#security-and-legal-considerations).

## Examples

### Network Inventory

```python
from kn_sock.network import arp_scan

def network_inventory():
    """Create a simple network inventory."""
    devices = arp_scan("192.168.1.0/24", verbose=True)
    
    print(f"Network Inventory - Found {len(devices)} devices:")
    print("-" * 50)
    
    for i, device in enumerate(devices, 1):
        print(f"{i:2d}. IP: {device['ip']:15s} MAC: {device['mac']}")

if __name__ == "__main__":
    network_inventory()
```

### Continuous Monitoring

```python
import time
from kn_sock.network import arp_scan

def monitor_network():
    """Monitor network for new devices."""
    known_devices = set()
    
    while True:
        current_devices = arp_scan("192.168.1.0/24")
        current_ips = {device['ip'] for device in current_devices}
        
        # Find new devices
        new_devices = current_ips - known_devices
        if new_devices:
            print(f"New devices detected: {new_devices}")
        
        # Find disconnected devices
        disconnected = known_devices - current_ips
        if disconnected:
            print(f"Devices disconnected: {disconnected}")
        
        known_devices = current_ips
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    monitor_network()
```

### Integration with MAC Lookup

```python
from kn_sock.network import arp_scan, mac_lookup

def detailed_network_scan():
    """Scan network and identify device vendors."""
    devices = arp_scan("192.168.1.0/24")
    
    for device in devices:
        # Lookup vendor information
        vendor_info = mac_lookup(device['mac'], use_api=False)
        
        print(f"IP: {device['ip']}")
        print(f"MAC: {device['mac']}")
        print(f"Vendor: {vendor_info['vendor']}")
        print("-" * 40)

if __name__ == "__main__":
    detailed_network_scan()
```
