# MAC Address Lookup

MAC address lookup allows you to identify device vendors and manufacturers by analyzing the Organizationally Unique Identifier (OUI) in MAC addresses.

⚠️ **ETHICAL WARNING**: MAC address lookup is intended for legitimate network management purposes only. This tool should only be used in authorized networks for device identification and network administration.

## Features

- **Vendor Identification**: Identify device manufacturers from MAC addresses
- **Online API Integration**: Use macvendors.co API for comprehensive database
- **Offline Mode**: Built-in OUI database for offline operation
- **Batch Processing**: Lookup multiple MAC addresses efficiently
- **Format Validation**: Validate MAC address formats
- **API Key Support**: Use API keys for higher rate limits

## Installation

MAC lookup requires the `requests` library for online lookups:

```bash
pip install requests
```

For complete dependency information, see the [API Reference](api-reference.md#dependencies).

## Basic Usage

### Python API

```python
from kn_sock.network import mac_lookup

# Lookup a single MAC address
result = mac_lookup("00:1A:2B:3C:4D:5E")
print(f"Vendor: {result['vendor']}")
print(f"OUI: {result['oui']}")
```

### Command Line

```bash
# Basic lookup
knsock mac-lookup 00:1A:2B:3C:4D:5E

# Offline mode only
knsock mac-lookup 00:1A:2B:3C:4D:5E --offline

# With API key
knsock mac-lookup 00:1A:2B:3C:4D:5E --api-key YOUR_API_KEY
```

For complete CLI documentation, see the [API Reference](api-reference.md#cli-commands).

## Advanced Usage

### Online vs Offline Lookup

```python
from kn_sock.network import mac_lookup

# Online lookup (default)
result = mac_lookup("00:1A:2B:3C:4D:5E", use_api=True)

# Offline lookup only
result = mac_lookup("00:1A:2B:3C:4D:5E", use_api=False)
```

### Batch Processing

```python
from kn_sock.network.mac_lookup import batch_mac_lookup

# Lookup multiple MAC addresses
macs = [
    "00:1A:2B:3C:4D:5E",
    "08:00:27:12:34:56",
    "52:54:00:AB:CD:EF"
]

results = batch_mac_lookup(macs)
for result in results:
    print(f"{result['mac']}: {result['vendor']}")
```

### MAC Address Validation

```python
from kn_sock.network.mac_lookup import validate_mac

# Validate MAC address format
macs = [
    "00:1A:2B:3C:4D:5E",  # Valid
    "00-1A-2B-3C-4D-5E",  # Valid
    "001A2B3C4D5E",        # Valid
    "00:1A:2B:3C:4D",     # Invalid (too short)
    "invalid-mac"          # Invalid
]

for mac in macs:
    is_valid = validate_mac(mac)
    print(f"{mac}: {'Valid' if is_valid else 'Invalid'}")
```

### API Key Usage

```python
from kn_sock.network.mac_lookup import mac_lookup_api

# Use API key for higher rate limits
result = mac_lookup_api("00:1A:2B:3C:4D:5E", api_key="YOUR_API_KEY")
```

## Function Reference

For complete API documentation, see the [API Reference](api-reference.md#mac-address-lookup-functions).

## MAC Address Formats

The lookup functions accept various MAC address formats:

| Format | Example | Description |
|--------|---------|-------------|
| Colon-separated | `00:1A:2B:3C:4D:5E` | Standard format |
| Hyphen-separated | `00-1A-2B-3C-4D-5E` | Alternative format |
| No separators | `001A2B3C4D5E` | Compact format |
| Mixed case | `00:1a:2b:3c:4d:5e` | Case insensitive |

## Common OUI Examples

| OUI | Vendor | Description |
|-----|--------|-------------|
| `00:50:56` | VMware, Inc. | Virtual machines |
| `08:00:27` | Oracle VirtualBox | Virtual machines |
| `52:54:00` | QEMU | Virtual machines |
| `00:15:5D` | Microsoft Corporation | Hyper-V |
| `00:16:3E` | Xen | Virtual machines |
| `AC:DE:48` | Private | Locally administered |

## Troubleshooting

### API Rate Limits

If you encounter rate limiting:

1. **Use API Key**: Get a free API key from macvendors.co
2. **Switch to Offline Mode**: Use built-in database
3. **Batch Processing**: Process multiple MACs in one request

```python
# Use API key
result = mac_lookup("00:1A:2B:3C:4D:5E", api_key="YOUR_API_KEY")

# Or use offline mode
result = mac_lookup("00:1A:2B:3C:4D:5E", use_api=False)
```

### Network Connectivity

For online lookups, ensure internet connectivity:

```python
import requests

try:
    response = requests.get("https://api.macvendors.com/00:1A:2B", timeout=5)
    print("API is accessible")
except requests.RequestException:
    print("API not accessible, using offline mode")
    result = mac_lookup("00:1A:2B:3C:4D:5E", use_api=False)
```

### Invalid MAC Addresses

Validate MAC addresses before lookup:

```python
from kn_sock.network.mac_lookup import validate_mac

mac = "00:1A:2B:3C:4D:5E"
if validate_mac(mac):
    result = mac_lookup(mac)
else:
    print("Invalid MAC address format")
```

## Security Considerations

1. **Privacy**: MAC addresses can reveal device information
2. **Network Security**: Use for legitimate network administration only
3. **Data Protection**: Be mindful of collected MAC address data
4. **API Keys**: Keep API keys secure and don't share them

For complete security and legal information, see the [API Reference](api-reference.md#security-and-legal-considerations).

## Examples

### Network Device Inventory

```python
from kn_sock.network import arp_scan, mac_lookup

def device_inventory():
    """Create detailed device inventory with vendor information."""
    # Scan network for devices
    devices = arp_scan("192.168.1.0/24")
    
    print("Network Device Inventory")
    print("=" * 60)
    
    for device in devices:
        # Lookup vendor information
        vendor_info = mac_lookup(device['mac'], use_api=False)
        
        print(f"IP Address: {device['ip']}")
        print(f"MAC Address: {device['mac']}")
        print(f"Vendor: {vendor_info['vendor']}")
        print(f"OUI: {vendor_info['oui']}")
        print("-" * 40)

if __name__ == "__main__":
    device_inventory()
```

### Virtual Machine Detection

```python
from kn_sock.network import arp_scan, mac_lookup

def detect_virtual_machines():
    """Identify virtual machines on the network."""
    devices = arp_scan("192.168.1.0/24")
    vm_ouis = ["00:50:56", "08:00:27", "52:54:00", "00:15:5D", "00:16:3E"]
    
    print("Virtual Machine Detection")
    print("=" * 40)
    
    for device in devices:
        vendor_info = mac_lookup(device['mac'], use_api=False)
        oui = vendor_info['oui']
        
        if oui in vm_ouis:
            print(f"VM Detected: {device['ip']} ({vendor_info['vendor']})")
        else:
            print(f"Physical Device: {device['ip']} ({vendor_info['vendor']})")

if __name__ == "__main__":
    detect_virtual_machines()
```

### MAC Address Validation Tool

```python
from kn_sock.network.mac_lookup import validate_mac, mac_lookup

def validate_and_lookup():
    """Validate MAC addresses and lookup vendor information."""
    test_macs = [
        "00:1A:2B:3C:4D:5E",
        "00-1A-2B-3C-4D-5E",
        "001A2B3C4D5E",
        "00:1A:2B:3C:4D",  # Invalid
        "invalid-mac"       # Invalid
    ]
    
    for mac in test_macs:
        print(f"MAC: {mac}")
        
        if validate_mac(mac):
            try:
                result = mac_lookup(mac, use_api=False)
                print(f"  Status: Valid")
                print(f"  Vendor: {result['vendor']}")
                print(f"  OUI: {result['oui']}")
            except Exception as e:
                print(f"  Status: Valid format, lookup failed: {e}")
        else:
            print(f"  Status: Invalid format")
        
        print("-" * 30)

if __name__ == "__main__":
    validate_and_lookup()
```

### Batch Processing with Error Handling

```python
from kn_sock.network.mac_lookup import batch_mac_lookup

def batch_lookup_with_errors():
    """Process multiple MAC addresses with error handling."""
    macs = [
        "00:1A:2B:3C:4D:5E",  # Valid
        "08:00:27:12:34:56",  # Valid
        "invalid-mac",        # Invalid
        "52:54:00:AB:CD:EF"   # Valid
    ]
    
    results = batch_mac_lookup(macs, use_api=False)
    
    print("Batch MAC Lookup Results")
    print("=" * 50)
    
    for i, result in enumerate(results):
        mac = macs[i]
        print(f"MAC: {mac}")
        
        if "Error" in result['vendor']:
            print(f"  Status: Error - {result['vendor']}")
        else:
            print(f"  Status: Success")
            print(f"  Vendor: {result['vendor']}")
            print(f"  OUI: {result['oui']}")
        
        print("-" * 30)

if __name__ == "__main__":
    batch_lookup_with_errors()
```
