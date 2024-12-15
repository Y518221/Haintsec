
"""
Performs a port scan on the target domain using Nmap.
Returns a dictionary mapping hosts to their open ports, or logs errors if the scan fails.
"""

import nmap
from urllib.parse import urlparse
import logging
import sys
from colorama import Fore, Style

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
        print(f"{Fore.BLUE}[*] Scanning {domain} for open {protocol.upper()} ports in range {port_range}...{Style.RESET_ALL}")
        nm.scan(domain, port_range, arguments=scan_type)

        # Check for open ports
        for host in nm.all_hosts():
            if protocol in nm[host]:
                open_ports[host] = nm[host][protocol]
        
        if not open_ports:
            print(f"{Fore.RED}[*] No open ports found.{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[*] Found open ports for {domain}:{Style.RESET_ALL}")
            for host, ports in open_ports.items():
                # Print each host's ports in a structured way
                print(f"{Fore.YELLOW}Host: {host}{Style.RESET_ALL}")
                for port, port_details in ports.items():
                    # Extract details for each port, checking if each field exists
                    state = port_details.get('state', 'N/A')
                    name = port_details.get('name', 'N/A')
                    reason = port_details.get('reason', 'N/A')
                    product = port_details.get('product', 'N/A')
                    version = port_details.get('version', 'N/A')
                    extra_info = port_details.get('extrainfo', 'N/A')
                    confidence = port_details.get('conf', 'N/A')

                    # Color code based on the state (open/closed)
                    if state == 'open':
                        port_color = Fore.GREEN
                    else:
                        port_color = Fore.RED

                    # Print each port's detailed information
                    print(f"{port_color}    Port: {port} ({name}) - State: {state.capitalize()}")
                    print(f"        Reason: {reason.capitalize()}")
                    print(f"        Product: {product}")
                    print(f"        Version: {version}")
                    print(f"        Extra Info: {extra_info}")
                    print(f"        Confidence: {confidence}")
                    print(f"{Style.RESET_ALL}")  # Reset the color

    except nmap.nmap.PortScannerError as e:
        print(f"{Fore.RED}[!] Port scanning error: {e}{Style.RESET_ALL}")
        logging.error(f"Port scanning error: {e}")
    except Exception as e:
        print(f"{Fore.RED}[!] An unexpected error occurred during the scan: {e}{Style.RESET_ALL}")
        logging.error(f"Unexpected error: {e}")
    
    return open_ports
