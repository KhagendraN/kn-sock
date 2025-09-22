"""
MAC address vendor lookup functionality.

⚠️  WARNING: This module is intended for use in authorized networks such as schools, 
labs, or controlled IT environments. MAC address lookup should only be used for 
legitimate network management purposes. Use responsibly and ethically.
"""

import json
import logging
import re
import requests
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

# Ethical warning message
ETHICAL_WARNING = """
⚠️  ETHICAL WARNING: MAC address lookup is intended for legitimate network 
management purposes only. This tool should only be used in authorized networks 
for device identification and network administration. Use responsibly and ethically.
"""


def _normalize_mac(mac: str) -> str:
    """Normalize MAC address to standard format (AA:BB:CC:DD:EE:FF)."""
    # Remove all non-hex characters and convert to uppercase
    mac_clean = re.sub(r'[^0-9A-Fa-f]', '', mac.upper())
    
    # Validate length
    if len(mac_clean) != 12:
        raise ValueError(f"Invalid MAC address: {mac} (must be 12 hex characters)")
    
    # Format as AA:BB:CC:DD:EE:FF
    return ':'.join([mac_clean[i:i+2] for i in range(0, 12, 2)])


def _get_oui_from_mac(mac: str) -> str:
    """Extract OUI (first 3 bytes) from MAC address."""
    normalized = _normalize_mac(mac)
    return normalized[:8]  # First 3 bytes (6 hex chars + 2 colons)


def mac_lookup_api(mac: str, api_key: Optional[str] = None) -> Dict[str, str]:
    """
    Lookup MAC address vendor using macvendors.co API.
    
    Args:
        mac: MAC address to lookup
        api_key: Optional API key for higher rate limits
        
    Returns:
        Dictionary containing vendor information
        
    Raises:
        ValueError: If MAC address is invalid
        requests.RequestException: If API request fails
    """
    print(ETHICAL_WARNING)
    
    try:
        oui = _get_oui_from_mac(mac)
    except ValueError as e:
        raise ValueError(f"Invalid MAC address: {e}")
    
    url = f"https://api.macvendors.com/{oui}"
    headers = {}
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        vendor = response.text.strip()
        
        return {
            "mac": _normalize_mac(mac),
            "oui": oui,
            "vendor": vendor,
            "source": "macvendors.co API"
        }
    
    except requests.RequestException as e:
        raise requests.RequestException(f"API lookup failed: {e}")


def mac_lookup_offline(mac: str) -> Dict[str, str]:
    """
    Lookup MAC address vendor using built-in OUI database.
    
    Args:
        mac: MAC address to lookup
        
    Returns:
        Dictionary containing vendor information
    """
    print(ETHICAL_WARNING)
    
    try:
        oui = _get_oui_from_mac(mac)
    except ValueError as e:
        raise ValueError(f"Invalid MAC address: {e}")
    
    # Common OUI database (simplified)
    oui_database = {
        "00:50:56": "VMware, Inc.",
        "00:0C:29": "VMware, Inc.",
        "00:1C:14": "VMware, Inc.",
        "00:15:5D": "Microsoft Corporation",
        "00:16:3E": "Xen",
        "08:00:27": "Oracle VirtualBox",
        "52:54:00": "QEMU",
        "AC:DE:48": "Private",
        "00:00:00": "Unknown",
        "FF:FF:FF": "Unknown (Broadcast)"
    }
    
    # Check for exact match
    if oui in oui_database:
        vendor = oui_database[oui]
    else:
        # Check for partial match (first 2 bytes)
        prefix = oui[:5]  # First 2 bytes
        vendor = "Unknown (not in local database)"
        
        for known_oui, known_vendor in oui_database.items():
            if known_oui.startswith(prefix):
                vendor = f"{known_vendor} (partial match)"
                break
    
    return {
        "mac": _normalize_mac(mac),
        "oui": oui,
        "vendor": vendor,
        "source": "local database"
    }


def mac_lookup(mac: str, use_api: bool = True, api_key: Optional[str] = None) -> Dict[str, str]:
    """
    Lookup MAC address vendor information.
    
    Args:
        mac: MAC address to lookup
        use_api: Whether to use online API (default: True)
        api_key: Optional API key for online lookup
        
    Returns:
        Dictionary containing vendor information
    """
    if use_api:
        try:
            return mac_lookup_api(mac, api_key)
        except Exception as e:
            logger.warning(f"API lookup failed: {e}, falling back to offline lookup")
            return mac_lookup_offline(mac)
    else:
        return mac_lookup_offline(mac)


def batch_mac_lookup(macs: List[str], use_api: bool = True, api_key: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Lookup multiple MAC addresses.
    
    Args:
        macs: List of MAC addresses to lookup
        use_api: Whether to use online API
        api_key: Optional API key for online lookup
        
    Returns:
        List of dictionaries containing vendor information
    """
    results = []
    
    for mac in macs:
        try:
            result = mac_lookup(mac, use_api, api_key)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to lookup MAC {mac}: {e}")
            results.append({
                "mac": mac,
                "oui": "Unknown",
                "vendor": f"Error: {e}",
                "source": "error"
            })
    
    return results


def validate_mac(mac: str) -> bool:
    """
    Validate MAC address format.
    
    Args:
        mac: MAC address to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        _normalize_mac(mac)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    # Example usage
    print("MAC Address Lookup Example")
    print("=" * 50)
    
    # Example MAC addresses
    test_macs = [
        "00:50:56:C0:00:08",  # VMware
        "08:00:27:12:34:56",  # VirtualBox
        "52:54:00:12:34:56",  # QEMU
        "invalid:mac:address"  # Invalid
    ]
    
    for mac in test_macs:
        print(f"\nLooking up: {mac}")
        if validate_mac(mac):
            try:
                result = mac_lookup(mac, use_api=False)  # Use offline for demo
                print(f"  Vendor: {result['vendor']}")
                print(f"  OUI: {result['oui']}")
                print(f"  Source: {result['source']}")
            except Exception as e:
                print(f"  Error: {e}")
        else:
            print("  Invalid MAC address format")
