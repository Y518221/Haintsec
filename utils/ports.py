
"""
Performs a port scan on the target domain using Nmap.
Returns a dictionary mapping hosts to their open ports, or logs errors if the scan fails.
"""

import nmap
from urllib.parse import urlparse
import logging
import sys

def scan_ports(url, port_range="1-65535", scan_type="-T4", protocol="tcp"):
    """
    Scan the target website for open ports and return the open ports.
    
    :param url: The URL of the target site to scan.
    :param port_range: The range of ports to scan (default is 1-65535).
    :param scan_type: The scan type (default is -T4, which is a faster scan).
    :param protocol: The protocol to scan (default is 'tcp').
    :return: A dictionary with hostnames as keys and a list of open ports as values.
    """
    domain = urlparse(url).netloc
    nm = nmap.PortScanner()
    open_ports = {}

    # Try scanning with error handling
    try:
        print(f"[*] Scanning {domain} for open {protocol.upper()} ports in range {port_range}...")
        nm.scan(domain, port_range, arguments=scan_type)
        
        for host in nm.all_hosts():
            if protocol in nm[host]:
                open_ports[host] = nm[host][protocol]
        
        if not open_ports:
            print("[*] No open ports found.")
        else:
            print(f"[*] Found open ports for {domain}:")
            for host, ports in open_ports.items():
                print(f"Host: {host} - Ports: {', '.join(map(str, ports.keys()))}")

    except nmap.nmap.PortScannerError as e:
        print(f"[!] Port scanning error: {e}")
        logging.error(f"Port scanning error: {e}")
    except Exception as e:
        print(f"[!] An unexpected error occurred during the scan: {e}")
        logging.error(f"Unexpected error: {e}")
    
    return open_ports
