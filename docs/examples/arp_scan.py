from kn_sock.network import arp_scan

# Example: Scan devices in subnet
if __name__ == "__main__":
    devices = arp_scan("192.168.1.0/24")
    for d in devices:
        print(f"IP: {d['ip']}, MAC: {d['mac']}")
