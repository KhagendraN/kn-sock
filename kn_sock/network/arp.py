"""
ARP scanning functionality for network device discovery.

⚠️  WARNING: This module is intended for use in authorized networks such as schools, 
labs, or controlled IT environments. ARP scanning may be considered intrusive and 
should only be used with proper authorization. Use responsibly and ethically.
"""

import logging
import socket
import subprocess
import sys
from typing import Dict, List, Optional, Tuple
from .mac_lookup import _normalize_mac, _get_oui_from_mac

# Optional third-party dependencies exposed at module level for test patching
try:
    import scapy.all as scapy  # type: ignore
except ImportError:  # pragma: no cover - environment dependent
    scapy = None  # type: ignore

try:
    import psutil  # type: ignore
except ImportError:  # pragma: no cover - environment dependent
    psutil = None  # type: ignore

logger = logging.getLogger(__name__)

# Ethical warning message
ETHICAL_WARNING = """
⚠️  ETHICAL WARNING: ARP scanning is intended for use in authorized networks only.
This tool should only be used in controlled IT environments, schools, or labs with 
proper authorization. Unauthorized network scanning may be illegal and unethical.
Use responsibly and ethically.
"""


def _check_scapy_available() -> bool:
    """Check if scapy is available for ARP scanning."""
    return scapy is not None


def _get_network_interface() -> Optional[str]:
    """Get the default network interface."""
    try:
        # Try to get the default route interface
        result = subprocess.run(
            ["ip", "route", "show", "default"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        for line in result.stdout.split('\n'):
            if 'default via' in line:
                parts = line.split()
                if len(parts) >= 5:
                    return parts[4]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Fallback to first available interface
    try:
        if psutil is None:
            raise ImportError
        interfaces = psutil.net_if_addrs()
        for interface_name, addresses in interfaces.items():
            for addr in addresses:
                if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                    return interface_name
    except ImportError:
        pass
    
    return None


def arp_scan(
    network_range: str, 
    interface: Optional[str] = None,
    timeout: int = 2,
    verbose: bool = False
) -> List[Dict[str, str]]:
    """
    Perform ARP scan on a network range to discover active devices.
    
    Args:
        network_range: Network range to scan (e.g., "192.168.1.0/24")
        interface: Network interface to use (auto-detect if None)
        timeout: Timeout in seconds for each ARP request
        verbose: Enable verbose logging
        
    Returns:
        List of dictionaries containing IP and MAC addresses of discovered devices
        
    Raises:
        ImportError: If scapy is not available
        ValueError: If network range is invalid
        RuntimeError: If scanning fails
    """
    print(ETHICAL_WARNING)
    
    if not _check_scapy_available():
        raise ImportError(
            "scapy is required for ARP scanning. Install it with: pip install scapy"
        )
    if scapy is None:  # safety
        raise ImportError("scapy not available")

    if verbose:
        logger.info(f"Starting ARP scan on {network_range}")
    
    # Validate network range format (CIDR notation)
    try:
        # Simple validation for CIDR format
        if '/' not in network_range:
            raise ValueError("Network range must be in CIDR format (e.g., 192.168.1.0/24)")
        ip_part, mask_part = network_range.split('/')
        
        # Validate IP part using socket
        import socket
        socket.inet_aton(ip_part)  # Will raise exception if invalid
        
        # Validate mask part
        mask = int(mask_part)
        if not 0 <= mask <= 32:
            raise ValueError("Network mask must be between 0 and 32")
    except Exception as e:
        raise ValueError(f"Invalid network range '{network_range}': {e}")
    
    # Auto-detect interface if not provided
    if interface is None:
        interface = _get_network_interface()
        if interface is None:
            raise RuntimeError("Could not auto-detect network interface")
        if verbose:
            logger.info(f"Using network interface: {interface}")
    
    devices = []
    
    try:
        # Create ARP request packet
        arp_request = scapy.ARP(pdst=network_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        
        if verbose:
            logger.info(f"Sending ARP requests to {network_range} via {interface}")
        
        # Send ARP requests and capture responses
        answered_list = scapy.srp(
            arp_request_broadcast, 
            iface=interface, 
            timeout=timeout, 
            verbose=False
        )[0]
        
        for element in answered_list:
            recv_pkt = element[1]
            device = {
                "ip": recv_pkt.psrc,
                "mac": recv_pkt.hwsrc,
                "interface": interface
            }
            devices.append(device)
            
            if verbose:
                logger.info(f"Found device: {device['ip']} -> {device['mac']}")
    
    except Exception as e:
        raise RuntimeError(f"ARP scan failed: {e}")
    
    if verbose:
        logger.info(f"ARP scan completed. Found {len(devices)} devices")
    
    return devices


def arp_scan_simple(ip_range: str) -> List[Tuple[str, str]]:
    """
    Simple ARP scan that returns IP and MAC pairs.
    
    Args:
        ip_range: IP range to scan (e.g., "192.168.1.0/24")
        
    Returns:
        List of tuples containing (IP, MAC) pairs
    """
    devices = arp_scan(ip_range)
    return [(device["ip"], device["mac"]) for device in devices]


def get_local_network_info() -> Dict[str, str]:
    """
    Get information about the local network.
    
    Returns:
        Dictionary containing network information
    """
    try:
        if psutil is None:
            raise ImportError
        # Get default gateway
        gateway = None
        try:
            result = subprocess.run(
                ["ip", "route", "show", "default"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            for line in result.stdout.split('\n'):
                if 'default via' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        gateway = parts[2]
                    break
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Get local IP and interface
        local_ip = None
        interface = None
        
        for interface_name, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                    local_ip = addr.address
                    interface = interface_name
                    break
            if local_ip:
                break
        
        return {
            "local_ip": local_ip or "Unknown",
            "interface": interface or "Unknown", 
            "gateway": gateway or "Unknown"
        }
    
    except ImportError:
        return {
            "local_ip": "Unknown (psutil not available)",
            "interface": "Unknown (psutil not available)",
            "gateway": "Unknown (psutil not available)"
        }


if __name__ == "__main__":
    # Example usage
    print("ARP Scanner Example")
    print("=" * 50)
    
    # Get local network info
    info = get_local_network_info()
    print(f"Local IP: {info['local_ip']}")
    print(f"Interface: {info['interface']}")
    print(f"Gateway: {info['gateway']}")
    print()
    
    # Example scan (replace with your network range)
    try:
        devices = arp_scan("192.168.1.0/24", verbose=True)
        print(f"\nFound {len(devices)} devices:")
        for device in devices:
            print(f"  {device['ip']} -> {device['mac']}")
    except Exception as e:
        print(f"Scan failed: {e}")
