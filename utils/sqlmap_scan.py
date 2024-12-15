# HaintSec - SQLMap Integration Module
#
# Purpose:
# This file is a module of the HaintSec vulnerability scanner tool, responsible for integrating SQLMap functionality. 
# SQLMap is an automated tool used to detect and exploit SQL injection vulnerabilities in web applications.
#
# Key Functionalities:
# - Executes SQLMap against a target URL.
# - Captures and returns results from SQLMap for further processing or reporting.
# - Provides real-time feedback and error handling during the execution of SQLMap.
#
# Dependencies:
# - SQLMap: Ensure the tool is installed and accessible in the system PATH or specify its path in the configuration.
# - Python Libraries: Requires `subprocess` for process handling and `colorama` for colored terminal output.


import subprocess
from colorama import Fore, Style

def run_sqlmap(url, sqlmap_path="sqlmap"):
    """
    Run SQLMap against the given URL and return the results.
    :param url: Target URL to test.
    :param sqlmap_path: Path to the SQLMap executable.
    :return: Parsed SQLMap results as a list of strings.
    """
    results = []
    try:
        print(f"{Fore.BLUE}[*] Starting SQLMap scan on {url}...{Style.RESET_ALL}")
        sqlmap_command = [sqlmap_path, "-u", url, "--batch", "--level=2"]
        process = subprocess.Popen(sqlmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in process.stdout:
            print(line.strip())  # Optional: print real-time output for debug
            results.append(line.strip())

        process.wait()

        if process.returncode == 0:
            print(f"{Fore.GREEN}[*] SQLMap scan completed successfully.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] SQLMap encountered an error.{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}[!] SQLMap not found at the specified path: {sqlmap_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] An error occurred during SQLMap execution: {e}{Style.RESET_ALL}")
    return results