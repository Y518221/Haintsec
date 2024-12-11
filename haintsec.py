import os
import time
import json
import argparse
import shutil
import logging
import subprocess
import sys
import importlib

from utils.subdomain import enumerate_subdomains
from utils.vulnerability import scan_website
from utils.ports import scan_ports
from utils.ssl_check import check_ssl
from utils.report import generate_report

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
        "PROXY": None  # Default to None if not provided
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            logging.error(f"Error loading config file: {e}. Using default configuration.")
            print(f"[!] Error loading config file: {e}. Using default configuration.")
    return default_config

CONFIG = load_config()

# Ensure output directory exists
OUTPUT_DIR = CONFIG.get("OUTPUT_DIR", "reports")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def install_python_dependencies():
    """
    Automatically install missing Python dependencies and notify the user.
    """
    print("[*] Checking Python dependencies...")
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

    # Check for missing packages
    for package, module in required_packages.items():
        try:
            importlib.import_module(module)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"[!] Missing packages detected: {', '.join(missing_packages)}")
        print("[*] Attempting to install missing packages...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
            print("[*] Installation completed.")
            print("[*] Restarting tool...")
            subprocess.run([sys.executable, __file__] + sys.argv)
            sys.exit()
        except Exception as e:
            print(f"[!] Failed to install packages: {e}")
            sys.exit(1)
    else:
        print("[*] All Python dependencies are satisfied.")


def validate_tools():
    missing_tools = []
    if not CONFIG.get("NMAP_PATH"):
        missing_tools.append("Nmap")
    if not shutil.which(CONFIG.get("SUBDOMAIN_TOOL", "")):
        missing_tools.append("Sublist3r")
    if not shutil.which(CONFIG.get("WKHTMLTOPDF_TOOL", "")):
        missing_tools.append("wkhtmltopdf")

    if missing_tools:
        logging.error(f"Missing required tools: {', '.join(missing_tools)}")
        print(f"[!] Missing required tools: {', '.join(missing_tools)}")
        print("Please install the missing tools and ensure they are available in the PATH.")
        exit(1)

def validate_config():
    """
    Ensure configuration values are valid and report issues.
    """
    print("[*] Validating configuration...")
    for key, value in CONFIG.items():
        if key != "PROXY" and not value:  # Skip validation for optional PROXY
            print(f"[!] Missing configuration: {key}. Check the {CONFIG_FILE} file.")
            exit(1)
    print("[*] Configuration is valid.")

def display_banner():
    print("=" * 99)
    print(" " * 35 + "HaintSec")
    print("=" * 99)
    print(f"Tool Developed by: {AUTHOR_NAME}")
    print(f"GitHub: {GITHUB_URL}")
    print(f"LinkedIn: {LINKEDIN_URL}")
    print("=" * 99)

def main():
    # Display the banner when the tool starts
    display_banner()

    # Pre-run checks
    install_python_dependencies()
    validate_tools()
    validate_config()

    # Setup argument parsing for the target URL
    parser = argparse.ArgumentParser(description="HaintSec Vulnerability Scanner")
    parser.add_argument("--url", required=True, help="Target URL (e.g., https://www.example.com)")
    args = parser.parse_args()
    url = args.url.strip()

    # Validate URL
    if not url.startswith(("http://", "https://")):
        print("[!] URL must start with http:// or https://. Prepending https://")
        url = "https://" + url

    print("=" * 99)
    print(f"Scanning target: {url}")
    print("=" * 99)

    # Measure the start time for performance tracking
    start_time = time.time()

    try:
        # Step 1: Subdomain Enumeration
        print("[*] Starting subdomain enumeration...")
        subdomains = enumerate_subdomains(url)
        logging.info("Subdomain enumeration completed.")

        # Step 2: Vulnerability Scanning
        print("[*] Scanning for vulnerabilities...")
        vulnerabilities = scan_website(url)
        logging.info("Vulnerability scanning completed.")

        # Step 3: Port Scanning
        print("[*] Performing port scanning...")
        open_ports = scan_ports(url)
        logging.info("Port scanning completed.")

        # Step 4: SSL/TLS Check
        print("[*] Checking SSL/TLS configuration...")
        ssl_issues = check_ssl(url)
        logging.info("SSL/TLS check completed.")

        # Step 5: Generate Report
        print("[*] Generating report...")
        report_docx, report_pdf = generate_report(url, subdomains, vulnerabilities, open_ports, ssl_issues)
        logging.info(f"Reports generated: {report_docx}, {report_pdf}")

        # Output the result
        print(f"Reports saved as: {report_docx}, {report_pdf}")
        print(f"Total execution time: {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"[!] An error occurred: {e}")

if __name__ == "__main__":
    main()
