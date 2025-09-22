"""
DNS monitoring and network traffic analysis.

⚠️  WARNING: This module is intended for use in authorized networks such as schools, 
labs, or controlled IT environments. Monitoring user traffic may be illegal without 
explicit consent. Use responsibly and ethically.
"""

psutil = None  # will be imported lazily; defined for patching in tests

import json
import logging
import socket
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any

logger = logging.getLogger(__name__)

# Ethical warning message
ETHICAL_WARNING = """
⚠️  ETHICAL WARNING: DNS monitoring is intended for use in authorized networks only.
This tool should only be used in controlled IT environments, schools, or labs with 
proper authorization. Monitoring user traffic without consent may be illegal and 
unethical. Use responsibly and ethically.
"""


def _check_scapy_available() -> bool:
    """Check if scapy is available for packet sniffing."""
    try:
        import scapy.all as _scapy  # noqa: F401
        return True
    except ImportError:
        return False


def _check_privileges() -> bool:
    """Check if running with sufficient privileges for packet sniffing."""
    try:
        import os
        return os.geteuid() == 0 or os.name == 'nt'
    except AttributeError:
        return False


def monitor_dns(
    duration: int = 60,
    interface: Optional[str] = None,
    log_file: Optional[str] = None,
    callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    verbose: bool = False
) -> List[Dict[str, Any]]:
    """
    Monitor DNS requests on the network.
    
    Args:
        duration: Duration to monitor in seconds
        interface: Network interface to monitor (auto-detect if None)
        log_file: File to save DNS logs (JSON format)
        callback: Function to call for each DNS request
        verbose: Enable verbose logging
        
    Returns:
        List of DNS request records
        
    Raises:
        ImportError: If scapy is not available
        PermissionError: If insufficient privileges
        RuntimeError: If monitoring fails
    """
    print(ETHICAL_WARNING)
    
    if not _check_scapy_available():
        raise ImportError(
            "scapy is required for DNS monitoring. Install it with: pip install scapy"
        )
    
    if not _check_privileges():
        raise PermissionError(
            "Root privileges required for packet sniffing. Run with sudo or as administrator."
        )
    
    import scapy.all as scapy
    
    dns_requests = []
    start_time = time.time()
    
    def process_packet(packet):
        """Process individual packets for DNS requests."""
        try:
            # Check if packet has DNS layer
            if packet.haslayer(scapy.DNS) and packet.haslayer(scapy.IP):
                dns_layer = packet[scapy.DNS]
                ip_layer = packet[scapy.IP]
                
                # Only process DNS queries (not responses)
                if dns_layer.qr == 0:  # Query flag
                    domain = dns_layer.qd.qname.decode('utf-8').rstrip('.')
                    query_type = dns_layer.qd.qtype
                    
                    # Map query types to names
                    query_types = {
                        1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR",
                        15: "MX", 16: "TXT", 28: "AAAA", 33: "SRV"
                    }
                    
                    record = {
                        "timestamp": datetime.now().isoformat(),
                        "source_ip": ip_layer.src,
                        "destination_ip": ip_layer.dst,
                        "domain": domain,
                        "query_type": query_types.get(query_type, f"TYPE{query_type}"),
                        "raw_query_type": query_type
                    }
                    
                    dns_requests.append(record)
                    
                    if callback:
                        callback(record)
                    
                    if verbose:
                        logger.info(f"DNS Query: {ip_layer.src} -> {domain} ({record['query_type']})")
        
        except Exception as e:
            if verbose:
                logger.warning(f"Error processing packet: {e}")
    
    try:
        if verbose:
            logger.info(f"Starting DNS monitoring for {duration} seconds")
            if interface:
                logger.info(f"Using interface: {interface}")
        
        # Start packet sniffing
        scapy.sniff(
            iface=interface,
            filter="udp port 53",
            prn=process_packet,
            timeout=duration
        )
        
        if verbose:
            logger.info(f"DNS monitoring completed. Captured {len(dns_requests)} requests")
        
        # Save to log file if specified
        if log_file:
            with open(log_file, 'w') as f:
                json.dump(dns_requests, f, indent=2)
            if verbose:
                logger.info(f"DNS logs saved to: {log_file}")
        
        return dns_requests
    
    except Exception as e:
        raise RuntimeError(f"DNS monitoring failed: {e}")


def monitor_dns_async(
    duration: int = 60,
    interface: Optional[str] = None,
    log_file: Optional[str] = None,
    callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    verbose: bool = False
) -> threading.Thread:
    """
    Start DNS monitoring in a separate thread.
    
    Args:
        duration: Duration to monitor in seconds
        interface: Network interface to monitor
        log_file: File to save DNS logs
        callback: Function to call for each DNS request
        verbose: Enable verbose logging
        
    Returns:
        Thread object running the monitoring
    """
    def monitor_thread():
        try:
            monitor_dns(duration, interface, log_file, callback, verbose)
        except Exception as e:
            logger.error(f"DNS monitoring thread failed: {e}")
    
    thread = threading.Thread(target=monitor_thread, daemon=True)
    thread.start()
    return thread


def analyze_dns_logs(log_file: str) -> Dict[str, Any]:
    """
    Analyze DNS logs and provide statistics.
    
    Args:
        log_file: Path to DNS log file (JSON format)
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        with open(log_file, 'r') as f:
            dns_requests = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Log file not found: {log_file}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in log file: {log_file}")
    
    if not dns_requests:
        return {"total_requests": 0, "message": "No DNS requests found"}
    
    # Basic statistics
    total_requests = len(dns_requests)
    unique_domains = len(set(req["domain"] for req in dns_requests))
    unique_sources = len(set(req["source_ip"] for req in dns_requests))
    
    # Domain frequency
    domain_counts = {}
    for req in dns_requests:
        domain = req["domain"]
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    
    # Top domains
    top_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Query type distribution
    query_types = {}
    for req in dns_requests:
        qtype = req["query_type"]
        query_types[qtype] = query_types.get(qtype, 0) + 1
    
    # Source IP distribution
    source_counts = {}
    for req in dns_requests:
        source = req["source_ip"]
        source_counts[source] = source_counts.get(source, 0) + 1
    
    top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        "total_requests": total_requests,
        "unique_domains": unique_domains,
        "unique_sources": unique_sources,
        "top_domains": top_domains,
        "query_type_distribution": query_types,
        "top_sources": top_sources,
        "analysis_timestamp": datetime.now().isoformat()
    }


def get_network_interfaces() -> List[Dict[str, str]]:
    """
    Get list of available network interfaces.
    
    Returns:
        List of interface information
    """
    try:
        global psutil
        if psutil is None:
            try:
                import psutil as _psutil  # type: ignore
                psutil = _psutil
            except ImportError:
                return [{"name": "unknown", "ip": "unknown", "netmask": "unknown"}]
        
        interfaces = []
        try:
            addrs = psutil.net_if_addrs()
        except Exception:
            return [{"name": "unknown", "ip": "unknown", "netmask": "unknown"}]
        for interface_name, addresses in addrs.items():
            for addr in addresses:
                if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                    interfaces.append({
                        "name": interface_name,
                        "ip": addr.address,
                        "netmask": addr.netmask
                    })
                    break
        
        if not interfaces:
            return [{"name": "unknown", "ip": "unknown", "netmask": "unknown"}]
        
        return interfaces
    
    except ImportError:
        return [{"name": "unknown", "ip": "unknown", "netmask": "unknown"}]


if __name__ == "__main__":
    # Example usage
    print("DNS Monitor Example")
    print("=" * 50)
    
    # Check prerequisites
    if not _check_scapy_available():
        print("❌ scapy not available. Install with: pip install scapy")
        exit(1)
    
    if not _check_privileges():
        print("❌ Insufficient privileges. Run with sudo or as administrator.")
        exit(1)
    
    # Get available interfaces
    interfaces = get_network_interfaces()
    print("Available interfaces:")
    for iface in interfaces:
        print(f"  {iface['name']}: {iface['ip']}")
    
    # Example monitoring
    print(f"\nStarting DNS monitoring for 30 seconds...")
    print("Make some DNS requests (browse web, ping hosts) to see activity.")
    
    try:
        results = monitor_dns(
            duration=30,
            log_file="dns_log.json",
            verbose=True
        )
        
        print(f"\nCaptured {len(results)} DNS requests")
        
        # Analyze results
        if results:
            analysis = analyze_dns_logs("dns_log.json")
            print(f"\nAnalysis:")
            print(f"  Total requests: {analysis['total_requests']}")
            print(f"  Unique domains: {analysis['unique_domains']}")
            print(f"  Unique sources: {analysis['unique_sources']}")
            
            if analysis['top_domains']:
                print(f"\nTop domains:")
                for domain, count in analysis['top_domains'][:5]:
                    print(f"  {domain}: {count} requests")
    
    except Exception as e:
        print(f"Monitoring failed: {e}")
