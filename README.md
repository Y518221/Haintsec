
# HaintSec - Web Vulnerability Analysis Tool

HaintSec is a tool developed to scan and analyze the security of websites, focusing on subdomain enumeration, vulnerability scanning, open port scanning, SSL/TLS checks, and exploitation via SQL injection (using SQLMap).

## Features

- **Subdomain Enumeration**: Enumerates subdomains of the target URL using Sublist3r.
- **Vulnerability Scanning**: Scans the website for common vulnerabilities like form-based injection points.
- **Port Scanning**: Scans for open ports using Nmap.
- **SSL/TLS Check**: Verifies the SSL/TLS configuration of the target.
- **Exploitation**: Attempts to exploit SQL injection vulnerabilities using SQLMap.

## Requirements

- Python 3.x
- **Sublist3r** (for subdomain enumeration)
- **SQLMap** (for SQL injection testing)
- **Nmap** (for network port scanning)
- **PDFKit** (for generating PDF reports)
- **BeautifulSoup** (for HTML parsing)
- **requests** (for HTTP requests)

## Installation

### 1. Clone the repository:
   First, clone the repository to your local machine:
   ```bash
   git clone https://github.com/Y518221/haintsec.git
   cd haintsec
   ```

### 2. Install Dependencies:
   The project uses `pip` to manage dependencies. Run the following command to install the necessary libraries:
   ```bash
   pip install -r requirements.txt
   ```

   You can manually install the required libraries with:
   ```bash
   pip install requests beautifulsoup4 nmap pdfkit python-docx
   ```

### 3. Install External Tools:
   - **Sublist3r**: Install Sublist3r (for subdomain enumeration):
     ```bash
     git clone https://github.com/aboul3la/Sublist3r.git
     cd Sublist3r
     pip install -r requirements.txt
     ```

   - **SQLMap**: Download and set up SQLMap:
     ```bash
     git clone https://github.com/sqlmapproject/sqlmap.git
     cd sqlmap
     ```

   - **Nmap**: Ensure you have Nmap installed. For example, on Ubuntu:
     ```bash
     sudo apt install nmap
     ```

   - **PDFKit & wkhtmltopdf**: Install PDFKit and `wkhtmltopdf` (required for PDF report generation):
     - Install `wkhtmltopdf` from [here](https://wkhtmltopdf.org/downloads.html) based on your OS.
     - Install PDFKit:
       ```bash
       pip install pdfkit
       ```

## Usage

1. **Run the Tool:**
   To run the tool, simply execute the script:
   ```bash
   python haintsec.py --url exampel.com
   ```

2. **Input the Target URL:**
   When prompted, enter the target URL to analyze. For example:
   ```bash
   Enter the target URL (e.g., https://www.example.com): https://example.com
   ```

3. **Tool Workflow:**
   The tool will perform the following:
   - **Subdomain Enumeration**: Using Sublist3r, it will find any subdomains of the target URL.
   - **Vulnerability Scanning**: It will scan the website for vulnerabilities, such as form-based injections.
   - **Port Scanning**: It will scan for open ports on the target using Nmap.
   - **SSL/TLS Check**: It will verify SSL/TLS configurations.
   - **SQL Injection Exploitation**: If any vulnerabilities are found, SQLMap will attempt to exploit them.

4. **Reports:**
   After the analysis, the tool generates two reports:
   - **Word Document** (`.docx`)
   - **PDF Report** (`.pdf`)

   The reports are saved with the target domain name, for example:
   - `example_com_vulnerability_report.docx`
   - `example_com_vulnerability_report.pdf`

   These reports contain detailed information on the findings, including subdomains, vulnerabilities, open ports, SSL issues, and any exploitation attempts.

## Example Output

Here’s an example of how the output would look:

```
====================================================================================================
                                                HaintSec
====================================================================================================
Tool Developed by: Yassine Selmi
GitHub: https://github.com/Y518221
LinkedIn: https://www.linkedin.com/in/yassine-selmi-1ba600260/

[*] Target URL: https://example.com
[*] Enumerating subdomains...
[*] Subdomain enumeration completed in 3.45 seconds.
[*] Scanning website for vulnerabilities...
[*] Website analysis completed in 2.12 seconds.
[*] Scanning open ports...
[*] Port scanning completed in 1.98 seconds.
[*] Checking SSL/TLS configurations...
[*] SSL/TLS check completed in 0.67 seconds.
[*] Verifying and exploiting potential vulnerabilities...
[*] Exploitation completed in 5.32 seconds.
[*] Generating detailed report...
[*] Report generation completed in 2.11 seconds.

[+] Analysis complete. Total time: 15.54 seconds.
Reports saved as: example_com_vulnerability_report.docx, example_com_vulnerability_report.pdf

```

## Author Information

- **Author**: Yassine Selmi
- **GitHub**: [https://github.com/Y518221](https://github.com/Y518221)
- **LinkedIn**: [https://www.linkedin.com/in/yassine-selmi-1ba600260/](https://www.linkedin.com/in/yassine-selmi-1ba600260/)

## License

This project is licensed under the **Proprietary License for Enhanced Vulnerability Analysis Tool**. You are granted permission to use the software, but copying, modifying, redistributing, or reverse-engineering the source code is strictly prohibited. For more information, please refer to the [LICENSE](LICENSE) file.
