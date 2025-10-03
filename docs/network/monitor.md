# DNS Monitoring

DNS monitoring allows you to capture and analyze DNS requests on your network, providing insights into network activity and device behavior.

⚠️ **ETHICAL WARNING**: DNS monitoring is intended for use in authorized networks only. This tool should only be used in controlled IT environments, schools, or labs with proper authorization. Monitoring user traffic without consent may be illegal and unethical.

## Features

- **Real-time DNS Capture**: Monitor DNS requests as they happen
- **Detailed Query Information**: Capture source IP, domain, and query type
- **JSON Logging**: Save captured data for analysis
- **Statistical Analysis**: Analyze DNS patterns and trends
- **Asynchronous Monitoring**: Run monitoring in background threads
- **Interface Selection**: Choose specific network interfaces to monitor

## Installation

DNS monitoring requires the `scapy` library:

```bash
pip install scapy
```

**Note**: DNS monitoring requires root/administrator privileges for packet sniffing.

For complete dependency information, see the [API Reference](api-reference.md#dependencies).

## Basic Usage

### Python API

```python
from kn_sock.network import monitor_dns

# Monitor DNS for 30 seconds
# Note: Requires root privileges (run with sudo)
try:
    results = monitor_dns(duration=30)
    for result in results:
        print(f"{result['source_ip']} -> {result['domain']}")
except ImportError:
    print("scapy required: pip install scapy")
except PermissionError:
    print("Root privileges required: sudo python script.py")
```

### Command Line

```bash
# Basic monitoring (requires sudo)
sudo kn-sock monitor

# Monitor for 2 minutes with logging
sudo kn-sock monitor --duration 120 --log dns_log.json

# Verbose output
sudo kn-sock monitor --duration 60 --verbose
```

For complete CLI documentation, see the [API Reference](api-reference.md#cli-commands).

## Advanced Usage

### Logging to File

```python
from kn_sock.network import monitor_dns

# Save results to JSON file
results = monitor_dns(
    duration=60, 
    log_file="dns_log.json",
    verbose=True
)
```

### Asynchronous Monitoring

```python
from kn_sock.network.monitor import monitor_dns_async
import time

# Start monitoring in background
monitor_thread = monitor_dns_async(
    duration=120,
    log_file="background_dns.json"
)

# Do other work while monitoring
print("Monitoring started in background...")
time.sleep(5)

# Wait for monitoring to complete
monitor_thread.join()
print("Monitoring completed!")
```

### Custom Callback Function

```python
from kn_sock.network import monitor_dns

def dns_callback(result):
    """Process each DNS request in real-time."""
    print(f"DNS Query: {result['source_ip']} -> {result['domain']} ({result['query_type']})")

# Monitor with custom callback
results = monitor_dns(
    duration=60,
    callback=dns_callback,
    verbose=True
)
```

### Interface Selection

```python
from kn_sock.network.monitor import get_network_interfaces, monitor_dns

# Get available interfaces
interfaces = get_network_interfaces()
for iface in interfaces:
    print(f"Interface: {iface['name']}, IP: {iface['ip']}")

# Monitor specific interface
results = monitor_dns(
    duration=60,
    interface="eth0",
    verbose=True
)
```

## Log Analysis

### Basic Analysis

```python
from kn_sock.network.monitor import analyze_dns_logs

# Analyze captured DNS logs
analysis = analyze_dns_logs("dns_log.json")

print(f"Total requests: {analysis['total_requests']}")
print(f"Unique domains: {analysis['unique_domains']}")
print(f"Unique sources: {analysis['unique_sources']}")

# Top domains
print("\nTop domains:")
for domain, count in analysis['top_domains'][:5]:
    print(f"  {domain}: {count} requests")
```

### Advanced Analysis

```python
import json
from kn_sock.network.monitor import analyze_dns_logs

def detailed_analysis(log_file):
    """Perform detailed DNS log analysis."""
    analysis = analyze_dns_logs(log_file)
    
    print("DNS Analysis Report")
    print("=" * 50)
    print(f"Analysis Time: {analysis['analysis_timestamp']}")
    print(f"Total Requests: {analysis['total_requests']}")
    print(f"Unique Domains: {analysis['unique_domains']}")
    print(f"Unique Sources: {analysis['unique_sources']}")
    
    print("\nTop 10 Domains:")
    for i, (domain, count) in enumerate(analysis['top_domains'][:10], 1):
        print(f"  {i:2d}. {domain:30s} {count:4d} requests")
    
    print("\nTop 10 Sources:")
    for i, (source, count) in enumerate(analysis['top_sources'][:10], 1):
        print(f"  {i:2d}. {source:15s} {count:4d} requests")
    
    print("\nQuery Type Distribution:")
    for qtype, count in analysis['query_type_distribution'].items():
        print(f"  {qtype:6s}: {count:4d} requests")

if __name__ == "__main__":
    detailed_analysis("dns_log.json")
```

## Function Reference

For complete API documentation, see the [API Reference](api-reference.md#dns-monitoring-functions).

## DNS Query Types

| Type | Name | Description |
|------|------|-------------|
| 1 | A | IPv4 address |
| 2 | NS | Name server |
| 5 | CNAME | Canonical name |
| 6 | SOA | Start of authority |
| 12 | PTR | Pointer (reverse DNS) |
| 15 | MX | Mail exchange |
| 16 | TXT | Text record |
| 28 | AAAA | IPv6 address |
| 33 | SRV | Service record |

## Troubleshooting

### Permission Issues

DNS monitoring requires root privileges for packet sniffing:

```bash
# Linux/macOS
sudo kn-sock monitor --duration 60

# Or in Python
sudo python -c "from kn_sock.network import monitor_dns; monitor_dns(60)"
```

### No DNS Requests Captured

1. **Check Interface**: Ensure you're monitoring the correct network interface
2. **Network Activity**: Generate some DNS requests (browse web, ping hosts)
3. **Firewall**: Some systems may block packet capture
4. **Virtual Environment**: Ensure you're not in a restricted container

### Scapy Installation Issues

```bash
# Install scapy
pip install scapy

# Or with system package manager
sudo apt-get install python3-scapy  # Ubuntu/Debian
sudo yum install python3-scapy      # CentOS/RHEL
```

### Interface Detection

```python
from kn_sock.network.monitor import get_network_interfaces

interfaces = get_network_interfaces()
print("Available interfaces:")
for iface in interfaces:
    print(f"  {iface['name']}: {iface['ip']}")
```

## Security Considerations

1. **Authorization**: Only monitor networks you own or have permission to monitor
2. **Legal Compliance**: Ensure compliance with local privacy and surveillance laws
3. **Data Privacy**: Be mindful of sensitive information in DNS queries
4. **Privilege Requirements**: Requires elevated privileges for packet capture
5. **Network Impact**: Minimal impact on network performance

For complete security and legal information, see the [API Reference](api-reference.md#security-and-legal-considerations).