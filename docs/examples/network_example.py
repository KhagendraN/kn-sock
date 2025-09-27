#!/usr/bin/env python3
"""
Example from kn-sock documentation - Network Scanning

This is a working example that users can copy and run to test network functionality.
It auto-detects your network and scans for devices.

Usage: 
  Without sudo: python copy_this_example.py  (tests basic functionality)
  With sudo:    sudo python copy_this_example.py  (full ARP scanning)
"""

from kn_sock.network import arp_scan, mac_lookup
from kn_sock.network.arp import get_local_network_info

def main():
    print("kn-sock Network Example")
    print("=" * 30)
    
    # Step 1: Get network information
    print("1. Getting your network info...")
    info = get_local_network_info()
    print(f"   Your IP: {info['local_ip']}")
    print(f"   Interface: {info['interface']}")
    print(f"   Gateway: {info['gateway']}")
    
    # Step 2: Test MAC lookup
    print("\n2. Testing MAC address lookup...")
    test_mac = "00:50:56:C0:00:08"  # VMware MAC
    try:
        result = mac_lookup(test_mac, use_api=False)
        print(f"   MAC: {test_mac}")
        print(f"   Vendor: {result['vendor']}")
        print("   ✅ MAC lookup working!")
    except Exception as e:
        print(f"   ❌ MAC lookup error: {e}")
    
    # Step 3: Try ARP scanning
    print("\n3. Testing network scanning...")
    
    if info['local_ip'] == "Unknown":
        print("   ❌ Cannot detect network for scanning")
        return
        
    # Auto-detect network range
    ip_parts = info['local_ip'].split('.')
    network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    print(f"   Network to scan: {network}")
    
    try:
        # Quick scan with short timeout
        devices = arp_scan(network, timeout=1)
        
        if devices:
            print(f"   ✅ Found {len(devices)} device(s):")
            for i, device in enumerate(devices, 1):
                print(f"      {i}. {device['ip']} -> {device['mac']}")
        else:
            print("   No devices found (this is normal for isolated networks)")
            
    except Exception as e:
        if "Operation not permitted" in str(e):
            print("   ℹ️  ARP scanning requires root privileges")
            print("      Run with: sudo python copy_this_example.py")
        else:
            print(f"   ❌ ARP scan error: {e}")
    
    print("\n🎉 Example completed!")
    print("\nTo see more examples, check the documentation:")
    print("https://github.com/KhagendraN/kn-sock/docs/network/")

if __name__ == "__main__":
    main()
