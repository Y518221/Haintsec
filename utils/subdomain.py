
"""
Enumerates subdomains for a given domain using Sublist3r.
Returns a list of discovered subdomains or logs an error if the process fails.
"""

from urllib.parse import urlparse
import subprocess
import sys
import os
from colorama import Fore, Style 

def enumerate_subdomains(url):
    domain = urlparse(url).netloc
    subdomains = []
    output_file = "subdomains_output.txt"  # Output file to capture results

    try:
        # Run Sublist3r and save results to the output file
        result = subprocess.run(
            ["sublist3r", "-d", domain, "-o", output_file],  # Save output to file
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check if the output file is created
        if result.returncode != 0:
            print(f"{Fore.RED}[!] Error running Sublist3r: {result.stderr}{Style.RESET_ALL}")
            return subdomains

        # Check if the output file is created
        if os.path.exists(output_file):
            print(f"[*] Output file created: {output_file}")
            with open(output_file, 'r') as file:
                subdomains = file.readlines()

            # Clean up: Remove output file after reading
            os.remove(output_file)

        # Clean up newlines and spaces
        subdomains = [subdomain.strip() for subdomain in subdomains if subdomain.strip()]

        if not subdomains:
            print(f"{Fore.YELLOW}[*] No subdomains found.{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[*] Found {len(subdomains)} subdomains.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[!] Error during subdomain enumeration: {e}{Style.RESET_ALL}")

    return subdomains
