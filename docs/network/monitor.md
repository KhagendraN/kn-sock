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

> 📝 **Copy-paste example**: For a complete working example you can copy and run, see [`docs/examples/network_example.py`](../examples/network_example.py)

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

## Examples

### Real-time DNS Monitor with Error Handling

```python
from kn_sock.network import monitor_dns
from kn_sock.network.monitor import _check_scapy_available, _check_privileges

def real_time_monitor():
    """Monitor DNS requests in real-time with proper error handling."""
    
    # Check prerequisites
    if not _check_scapy_available():
        print("❌ Error: scapy not available")
        print("Install with: pip install scapy")
        return
    
    if not _check_privileges():
        print("❌ Error: Root privileges required")
        print("Run with: sudo python script.py")
        return
    
    def process_dns(result):
        """Process each DNS request."""
        domain = result['domain']
        source = result['source_ip']
        qtype = result['query_type']
        
        # Filter for interesting queries
        if any(keyword in domain for keyword in ["google", "facebook", "youtube"]):
            print(f"🌐 Popular site: {source} -> {domain} ({qtype})")
        elif domain.endswith('.local'):
            print(f"🏠 Local query: {source} -> {domain} ({qtype})")
        else:
            print(f"🔍 DNS Query: {source} -> {domain} ({qtype})")
    
    print("Starting real-time DNS monitoring...")
    print("Make some web requests to see DNS activity")
    print("Press Ctrl+C to stop\n")
    
    try:
        results = monitor_dns(
            duration=300,  # 5 minutes
            callback=process_dns,
            log_file="dns_monitoring.json",
            verbose=False  # Disable verbose to reduce noise
        )
        
        print(f"\n✅ Monitoring completed. Captured {len(results)} DNS requests.")
        
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Monitoring failed: {e}")

if __name__ == "__main__":
    real_time_monitor()
```

### Network Activity Dashboard

```python
import time
from kn_sock.network import monitor_dns
from kn_sock.network.monitor import analyze_dns_logs, _check_scapy_available, _check_privileges

def activity_dashboard():
    """Create a simple network activity dashboard."""
    
    # Check prerequisites
    if not _check_scapy_available():
        print("❌ scapy not available. Install with: pip install scapy")
        return
        
    if not _check_privileges():
        print("❌ Root privileges required. Run with: sudo python script.py")
        return
    
    log_file = "network_activity.json"
    
    print("Network Activity Dashboard")
    print("=" * 50)
    print("Monitoring network DNS activity...")
    print("Browse the web to generate DNS traffic\n")
    
    try:
        # Monitor for 2 minutes
        results = monitor_dns(
            duration=120,
            log_file=log_file,
            verbose=True
        )
        
        if not results:
            print("No DNS activity detected.")
            return
        
        # Analyze the results
        print(f"\n📊 Analysis Results:")
        print("=" * 30)
        
        analysis = analyze_dns_logs(log_file)
        
        print(f"📈 Total DNS Requests: {analysis['total_requests']}")
        print(f"🌐 Unique Domains: {analysis['unique_domains']}")
        print(f"💻 Unique Sources: {analysis['unique_sources']}")
        
        # Show top domains
        if analysis['top_domains']:
            print(f"\n🔝 Top Domains:")
            for i, (domain, count) in enumerate(analysis['top_domains'][:10], 1):
                print(f"  {i:2d}. {domain:30s} ({count:3d} requests)")
        
        # Show query type distribution
        if analysis['query_type_distribution']:
            print(f"\n📋 Query Types:")
            for qtype, count in analysis['query_type_distribution'].items():
                print(f"  {qtype:6s}: {count:3d} requests")
        
        # Show top sources
        if analysis['top_sources']:
            print(f"\n💻 Top Source IPs:")
            for ip, count in analysis['top_sources'][:5]:
                print(f"  {ip:15s}: {count:3d} requests")
                
        print(f"\n💾 Full log saved to: {log_file}")
        
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    activity_dashboard()
```
    results = monitor_dns(duration=120, log_file=log_file)
    
    # Analyze results
    analysis = analyze_dns_logs(log_file)
    
    print(f"\nActivity Summary:")
    print(f"Total DNS requests: {analysis['total_requests']}")
    print(f"Active devices: {analysis['unique_sources']}")
    print(f"Unique domains: {analysis['unique_domains']}")
    
    print(f"\nMost active domains:")
    for domain, count in analysis['top_domains'][:5]:
        print(f"  {domain}: {count} requests")
    
    print(f"\nMost active devices:")
    for source, count in analysis['top_sources'][:5]:
        print(f"  {source}: {count} requests")

if __name__ == "__main__":
    activity_dashboard()
```

### Continuous Monitoring with Alerts

```python
import time
import json
from datetime import datetime
from kn_sock.network import monitor_dns

def continuous_monitor():
    """Continuous DNS monitoring with alerting."""
    alert_domains = ["malware.com", "phishing.net", "suspicious.org"]
    log_file = f"monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def alert_callback(result):
        domain = result['domain']
        source = result['source_ip']
        
        # Check for alert domains
        for alert_domain in alert_domains:
            if alert_domain in domain:
                alert_msg = f"ALERT: {source} accessed {domain} at {result['timestamp']}"
                print(f"🚨 {alert_msg}")
                
                # Log alert to file
                with open("alerts.log", "a") as f:
                    f.write(f"{alert_msg}\n")
    
    print("Starting continuous DNS monitoring...")
    print("Alert domains:", alert_domains)
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            print(f"\nMonitoring cycle started at {datetime.now()}")
            results = monitor_dns(
                duration=60,  # 1 minute cycles
                log_file=log_file,
                callback=alert_callback,
                verbose=False
            )
            
            print(f"Captured {len(results)} DNS requests")
            time.sleep(5)  # Brief pause between cycles
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

if __name__ == "__main__":
    continuous_monitor()
```

### DNS Query Type Analysis

```python
from kn_sock.network import monitor_dns, analyze_dns_logs

def query_type_analysis():
    """Analyze DNS query types and patterns."""
    print("DNS Query Type Analysis")
    print("=" * 30)
    
    # Monitor for 3 minutes
    results = monitor_dns(duration=180, log_file="query_analysis.json")
    
    # Analyze results
    analysis = analyze_dns_logs("query_analysis.json")
    
    print(f"Total queries: {analysis['total_requests']}")
    print(f"Query type distribution:")
    
    for qtype, count in analysis['query_type_distribution'].items():
        percentage = (count / analysis['total_requests']) * 100
        print(f"  {qtype:6s}: {count:4d} ({percentage:5.1f}%)")
    
    # Analyze by time patterns
    print(f"\nTop domains by query type:")
    for domain, count in analysis['top_domains'][:10]:
        print(f"  {domain}: {count} queries")

if __name__ == "__main__":
    query_type_analysis()
```
