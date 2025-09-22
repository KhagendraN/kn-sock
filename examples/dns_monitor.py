from kn_sock.network import monitor_dns

# Example: Monitor DNS for 60 seconds and log to file
if __name__ == "__main__":
    results = monitor_dns(duration=60, log_file="dns_log.json")
    for r in results:
        print(f"IP: {r['ip']}, Domain: {r['domain']}")
