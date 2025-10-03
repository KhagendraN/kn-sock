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

# Example with a real MAC address (VMware)
result = mac_lookup("00:50:56:C0:00:08")
print(f"MAC: {result['mac']}")
print(f"Vendor: {result['vendor']}")
print(f"OUI: {result['oui']}")

# Offline lookup only (faster, uses local database)
result = mac_lookup("00:50:56:C0:00:08", use_api=False)
print(f"Vendor: {result['vendor']}")
```

### Command Line

```bash
# Basic lookup
kn-sock mac-lookup 00:1A:2B:3C:4D:5E

# Offline mode only
kn-sock mac-lookup 00:1A:2B:3C:4D:5E --offline

# With API key
kn-sock mac-lookup 00:1A:2B:3C:4D:5E --api-key YOUR_API_KEY
```

For complete CLI documentation, see the [API Reference](api-reference.md#cli-commands).

## Advanced Usage

### Online vs Offline Lookup

```python
from kn_sock.network import mac_lookup

# Try online first, fallback to offline
mac = "00:50:56:C0:00:08"  # VMware MAC example

# Online lookup (with automatic fallback to offline)
result = mac_lookup(mac, use_api=True)
print(f"Online result: {result['vendor']} (Source: {result['source']})")

# Offline only (faster, uses local database)
result = mac_lookup(mac, use_api=False)
print(f"Offline result: {result['vendor']} (Source: {result['source']})")
```

### Batch Processing

```python
from kn_sock.network.mac_lookup import batch_mac_lookup

# Example MAC addresses from different vendors
macs = [
    "00:50:56:C0:00:08",  # VMware
    "08:00:27:12:34:56",  # VirtualBox  
    "52:54:00:AB:CD:EF"   # QEMU
]

results = batch_mac_lookup(macs, use_api=False)  # Use offline for speed
for result in results:
    print(f"{result['mac']}: {result['vendor']}")
```

### MAC Address Validation

```python
from kn_sock.network.mac_lookup import validate_mac

# Test different MAC address formats
test_macs = [
    "00:50:56:C0:00:08",     # Valid colon format
    "00-50-56-C0-00-08",     # Valid hyphen format
    "005056C00008",          # Valid compact format
    "00:50:56:c0:00:08",     # Valid mixed case
    "00:1A:2B:3C:4D",        # Invalid (too short)
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

