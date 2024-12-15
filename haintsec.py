#!/usr/bin/env python3
"""
Loads configuration values from a JSON file and sets default values if not provided.
Handles errors if the configuration file is missing or improperly formatted.
Checks and installs missing Python packages required for the tool.
Automatically installs dependencies and restarts the script if necessary.
Ensures that required external tools (e.g., Nmap, SQLMap, Sublist3r) are installed and accessible in the system PATH.
Logs and prints errors if any tools are missing.
The main entry point for the HaintSec tool.
Handles pre-run checks, parses command-line arguments, and orchestrates scanning operations.

"""

import argparse
from colorama import Fore, Style, init
import time
import logging
import sys
import subprocess
import shutil
import importlib
import json
import os

from utils.subdomain import enumerate_subdomains
from utils.vulnerability import scan_website
from utils.ports import scan_ports
from utils.ssl_check import check_ssl
from utils.report import generate_report
from utils.sqlmap_scan import run_sqlmap

# Initialize colorama
init(autoreset=True)

# --- Configuration ---
AUTHOR_NAME = "Yassine Selmi"
GITHUB_URL = "https://github.com/Y518221"
LINKEDIN_URL = "https://www.linkedin.com/in/yassine-selmi-1ba600260/"
CONFIG_FILE = "config.json"

# Set up logging
LOG_FILE = "haintsec.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("HaintSec started.")

def load_config():
    default_config = {
        "SQLMAP_PATH": "sqlmap",
        "NMAP_PATH": shutil.which("nmap"),
        "SUBDOMAIN_TOOL": "sublist3r",
        "WKHTMLTOPDF_TOOL": shutil.which("wkhtmltopdf"),
        "OUTPUT_DIR": "reports",
        "PROXY": None
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            logging.error(f"Error loading config file: {e}. Using default configuration.")
            print(f"{Fore.RED}[!] Error loading config file: {e}. Using default configuration.{Style.RESET_ALL}")
    return default_config

CONFIG = load_config()

# Ensure output directory exists
OUTPUT_DIR = CONFIG.get("OUTPUT_DIR", "reports")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def install_python_dependencies():
    print(f"{Fore.BLUE}[*] Checking Python dependencies...{Style.RESET_ALL}")
    required_packages = {
        "beautifulsoup4": "bs4",
        "requests": "requests",
        "python-nmap": "nmap",
        "python-docx": "docx",
        "pdfkit": "pdfkit",
        "argparse": "argparse",
        "urllib3": "urllib3",
    }
    missing_packages = []

    for package, module in required_packages.items():
        try:
            importlib.import_module(module)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"{Fore.RED}[!] Missing packages detected: {', '.join(missing_packages)}{Style.RESET_ALL}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
            print(f"{Fore.GREEN}[*] Installation completed. Restarting tool...{Style.RESET_ALL}")
            subprocess.run([sys.executable, __file__] + sys.argv)
            sys.exit()
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to install packages: {e}{Style.RESET_ALL}")
            sys.exit(1)
    else:
        print(f"{Fore.GREEN}[*] All Python dependencies are satisfied.{Style.RESET_ALL}")

def validate_tools():
    missing_tools = []
    if not CONFIG.get("NMAP_PATH"):
        missing_tools.append("Nmap")
    if not shutil.which(CONFIG.get("SUBDOMAIN_TOOL", "")):
        missing_tools.append("Sublist3r")
    if not shutil.which(CONFIG.get("WKHTMLTOPDF_TOOL", "")):
        missing_tools.append("wkhtmltopdf")
    if not shutil.which(CONFIG.get("SQLMAP_PATH", "")):
        missing_tools.append("SQLMap")

    if missing_tools:
        logging.error(f"Missing required tools: {', '.join(missing_tools)}")
        print(f"{Fore.RED}[!] Missing required tools: {', '.join(missing_tools)}. Please install them.{Style.RESET_ALL}")
        exit(1)
    else:
        print(f"{Fore.GREEN}[*] All required tools are available.{Style.RESET_ALL}")

def validate_config():
    print(f"{Fore.BLUE}[*] Validating configuration...{Style.RESET_ALL}")
    for key, value in CONFIG.items():
        if key != "PROXY" and not value:
            print(f"{Fore.RED}[!] Missing configuration: {key}.{Style.RESET_ALL}")
            exit(1)
    print(f"{Fore.GREEN}[*] Configuration is valid.{Style.RESET_ALL}")

def display_banner():
    print(f"{Fore.MAGENTA}{'=' * 99}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{' ' * 35}HaintSec{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'=' * 99}{Style.RESET_ALL}")
    print(f"Tool Developed by: {AUTHOR_NAME}")
    print(f"GitHub: {GITHUB_URL}")
    print(f"LinkedIn: {LINKEDIN_URL}")
    print(f"{Fore.MAGENTA}{'=' * 99}{Style.RESET_ALL}")

def main():
    display_banner()
    install_python_dependencies()
    validate_tools()
    validate_config()

    parser = argparse.ArgumentParser(description="HaintSec Vulnerability Scanner")
    parser.add_argument("--url", required=True, help="Target URL (e.g., https://www.example.com)")
    args = parser.parse_args()
    url = args.url.strip()

    if not url.startswith(("http://", "https://")):
        print(f"{Fore.YELLOW}[!] URL must start with http:// or https://. Prepending https://{Style.RESET_ALL}")
        url = "https://" + url

    start_time = time.time()
    try:
        print(f"{Fore.CYAN}{'=' * 99}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Scanning target: {url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 99}{Style.RESET_ALL}")
        
        # Subdomain enumeration
        print(f"{Fore.BLUE}[*] Starting subdomain enumeration...{Style.RESET_ALL}")
        subdomains = enumerate_subdomains(url)
        if subdomains:
            print(f"{Fore.BLUE}[*] Found subdomains:{Style.RESET_ALL} {', '.join(subdomains)}")
        else:
            print(f"{Fore.YELLOW}[*] No subdomains found.{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[*] Subdomain enumeration completed.{Style.RESET_ALL}")

        # Vulnerability scanning
        print(f"{Fore.BLUE}[*] Scanning for vulnerabilities...{Style.RESET_ALL}")
        vulnerabilities, html_content_vulnerabilities = scan_website(url)

        if vulnerabilities:
            for vuln in vulnerabilities:
                print(f"    - {vuln['type']}: {vuln['detail']}")
        else:
            print("[*] No vulnerabilities detected.")
        print(f"{Fore.BLUE}[*] Vulnerability scanning completed.{Style.RESET_ALL}")

        # Port scanning
        print(f"{Fore.BLUE}[*] Performing port scanning...{Style.RESET_ALL}")
        open_ports = scan_ports(url)
        
        if open_ports:
            print("")
            #print(f"[*] Open ports detected: {', '.join([f'{port} ({protocol})' for host, ports in open_ports.items() for port, protocol in ports.items()])}")
        else:
            print("[*] No open ports detected.")
        print(f"{Fore.BLUE}[*] Port scanning completed.{Style.RESET_ALL}")

        # SSL/TLS checking
        print(f"{Fore.BLUE}[*] Checking SSL/TLS configuration...{Style.RESET_ALL}")
        ssl_issues = check_ssl(url)

        if ssl_issues:
            for issue in ssl_issues:
                print(f"    - {issue}")
        else:
            print("[*] No SSL/TLS issues detected.")
        print(f"{Fore.BLUE}[*] SSL/TLS check completed.{Style.RESET_ALL}")

        # SQLMap scanning
        print(f"{Fore.BLUE}[*] Running SQLMap for advanced scanning...{Style.RESET_ALL}")
        sqlmap_results = run_sqlmap(url, CONFIG.get("SQLMAP_PATH"))

        if sqlmap_results:
            for result in sqlmap_results:
                print(f"    - {result}")
        else:
            print("[*] No SQL injection vulnerabilities detected.")
        print(f"{Fore.BLUE}[*] SQLMap scanning completed.{Style.RESET_ALL}")

        # Generating report
        print(f"{Fore.BLUE}[*] Generating report...{Style.RESET_ALL}")
        report_docx, report_pdf = generate_report(url, subdomains, vulnerabilities, open_ports, ssl_issues, sqlmap_results, html_content_vulnerabilities)
        logging.info(f"Reports generated: {report_docx}, {report_pdf}")

        print(f"{Fore.GREEN}[*] Reports saved as: {report_docx}, {report_pdf}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Total execution time: {time.time() - start_time:.2f} seconds{Style.RESET_ALL}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"{Fore.RED}[!] An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
