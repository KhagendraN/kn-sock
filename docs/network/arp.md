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
from kn_sock.network.arp import get_local_network_info

# Auto-detect and scan your actual network
info = get_local_network_info()
if info['local_ip'] != 'Unknown':
    ip_parts = info['local_ip'].split('.')
    network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    
    devices = arp_scan(network)
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}")
else:
    print("Could not auto-detect network. Please specify manually:")
    # devices = arp_scan("YOUR_NETWORK_HERE/24")  # e.g., 192.168.1.0/24
```

> 📝 **Copy-paste example**: For a complete working example you can copy and run, see [`docs/examples/network_example.py`](../examples/network_example.py)

### Command Line

```bash
# Basic scan
kn-sock scan 192.168.1.0/24

# Verbose output
kn-sock scan 192.168.1.0/24 --verbose

# Custom interface and timeout
kn-sock scan 192.168.1.0/24 --interface eth0 --timeout 5
```

For complete CLI documentation, see the [API Reference](api-reference.md#cli-commands).

## Advanced Usage

### Custom Interface Selection

```python
from kn_sock.network import arp_scan
from kn_sock.network.arp import get_local_network_info

# Auto-detect network first
info = get_local_network_info()
if info['local_ip'] != 'Unknown':
    ip_parts = info['local_ip'].split('.')
    network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    
    # Use detected interface or specify your own
    devices = arp_scan(network, interface=info['interface'])
    # or specify manually: devices = arp_scan(network, interface="eth0")
```

### Verbose Logging

```python
from kn_sock.network import arp_scan
from kn_sock.network.arp import get_local_network_info

# Auto-detect network and enable detailed logging
info = get_local_network_info()
if info['local_ip'] != 'Unknown':
    ip_parts = info['local_ip'].split('.')
    network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    
    devices = arp_scan(network, verbose=True)
```

### Simple IP/MAC Pairs

```python
from kn_sock.network.arp import arp_scan_simple, get_local_network_info

# Auto-detect network and get simple tuples
info = get_local_network_info()
if info['local_ip'] != 'Unknown':
    ip_parts = info['local_ip'].split('.')
    network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    
    device_pairs = arp_scan_simple(network)
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
sudo kn-sock scan 192.168.1.0/24
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

### Auto-Detect Network and Scan

```python
from kn_sock.network import arp_scan
from kn_sock.network.arp import get_local_network_info

def smart_network_scan():
    """Automatically detect and scan local network."""
    # Get local network information
    info = get_local_network_info()
    print(f"Local IP: {info['local_ip']}")
    print(f"Interface: {info['interface']}")
    print(f"Gateway: {info['gateway']}")
    
    # Auto-generate network range
    local_ip = info['local_ip']
    if local_ip != "Unknown" and '.' in local_ip:
        ip_parts = local_ip.split('.')
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        
        print(f"\nScanning network: {network_range}")
        devices = arp_scan(network_range, verbose=True)
        
        if devices:
            print(f"\n✅ Found {len(devices)} devices:")
            print("-" * 50)
            for i, device in enumerate(devices, 1):
                print(f"{i:2d}. IP: {device['ip']:15s} MAC: {device['mac']}")
        else:
            print("No devices found on this network.")
    else:
        print("Could not auto-detect network. Please specify manually.")

if __name__ == "__main__":
    smart_network_scan()
```

### Simple Network Inventory

```python
from kn_sock.network import arp_scan

def network_inventory(network_range="192.168.1.0/24"):
    """Create a simple network inventory."""
    try:
        devices = arp_scan(network_range, verbose=True)
        
        print(f"Network Inventory - Found {len(devices)} devices:")
        print("-" * 50)
        
        for i, device in enumerate(devices, 1):
            print(f"{i:2d}. IP: {device['ip']:15s} MAC: {device['mac']}")
            
    except RuntimeError as e:
        if "Operation not permitted" in str(e):
            print("❌ ARP scan requires root privileges. Run with sudo:")
            print("sudo python your_script.py")
        else:
            print(f"❌ Scan failed: {e}")

if __name__ == "__main__":
    network_inventory()
```

### Continuous Network Monitoring

```python
import time
from kn_sock.network import arp_scan
from kn_sock.network.arp import get_local_network_info

def monitor_network():
    """Monitor network for device changes."""
    # Auto-detect network range
    info = get_local_network_info()
    local_ip = info['local_ip']
    
    if local_ip == "Unknown":
        print("❌ Could not detect local network. Please specify manually.")
        return
    
    ip_parts = local_ip.split('.')
    network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    
    print(f"Monitoring network: {network_range}")
    print("Press Ctrl+C to stop monitoring\n")
    
    known_devices = set()
    scan_count = 0
    
    try:
        while True:
            scan_count += 1
            print(f"[Scan #{scan_count}] Checking network...")
            
            try:
                current_devices = arp_scan(network_range)
                current_ips = {device['ip'] for device in current_devices}
                
                # Find new devices
                new_devices = current_ips - known_devices
                if new_devices:
                    print(f"🔍 New devices detected: {new_devices}")
                
                # Find disconnected devices
                disconnected = known_devices - current_ips
                if disconnected:
                    print(f"📤 Devices disconnected: {disconnected}")
                
                known_devices = current_ips
                print(f"✅ Currently active: {len(current_ips)} devices")
                
            except Exception as e:
                print(f"❌ Scan failed: {e}")
            
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        print(f"\nMonitoring stopped after {scan_count} scans.")

if __name__ == "__main__":
    monitor_network()
```

### Integration with MAC Lookup

```python
from kn_sock.network import arp_scan, mac_lookup
from kn_sock.network.arp import get_local_network_info

def detailed_network_scan():
    """Scan network and identify device vendors."""
    # Auto-detect network
    info = get_local_network_info()
    local_ip = info['local_ip']
    
    if local_ip == "Unknown":
        network_range = "192.168.1.0/24"  # Fallback
        print(f"Using fallback network range: {network_range}")
    else:
        ip_parts = local_ip.split('.')
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        print(f"Scanning detected network: {network_range}")
    
    try:
        devices = arp_scan(network_range)
        
        if not devices:
            print("No devices found on network.")
            return
            
        print(f"\nDetailed Network Analysis - {len(devices)} devices found:")
        print("=" * 70)
        
        for i, device in enumerate(devices, 1):
            print(f"\n[Device #{i}]")
            print(f"IP Address: {device['ip']}")
            print(f"MAC Address: {device['mac']}")
            
            # Lookup vendor information
            try:
                vendor_info = mac_lookup(device['mac'], use_api=False)  # Use offline first
                print(f"Vendor: {vendor_info['vendor']}")
                print(f"OUI: {vendor_info['oui']}")
            except Exception as e:
                print(f"Vendor lookup failed: {e}")
            
            print("-" * 40)
            
    except Exception as e:
        if "Operation not permitted" in str(e):
            print("❌ Root privileges required. Run with: sudo python script.py")
        else:
            print(f"❌ Scan failed: {e}")

if __name__ == "__main__":
    detailed_network_scan()
```
