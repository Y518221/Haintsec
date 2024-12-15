
# HaintSec - Vulnerability Scanner

HaintSec is a security vulnerability scanner that helps identify potential security issues in websites. The tool runs several tests such as subdomain enumeration, vulnerability scanning, port scanning, SSL certificate validation, and SQL injection testing. It generates detailed reports in DOCX and PDF formats.

### Author:
- **Name**: Yassine Selmi  
- **GitHub**: [Y518221](https://github.com/Y518221)  
- **LinkedIn**: [Yassine Selmi](https://www.linkedin.com/in/yassine-selmi-1ba600260/)

---

## Features

- **Subdomain Enumeration**: Identifies subdomains associated with the target website.
- **Vulnerability Scanning**: Scans the website for common vulnerabilities.
- **Port Scanning**: Identifies open ports on the target website.
- **SSL Check**: Verifies SSL certificate validity and identifies potential issues.
- **SQL Injection Testing**: Uses SQLMap to detect SQL injection vulnerabilities.
- **Report Generation**: Generates comprehensive DOCX and PDF reports with all findings.

---

## Prerequisites

### Python Dependencies
The following Python libraries are required:
- **beautifulsoup4**
- **requests**
- **python-nmap**
- **python-docx**
- **pdfkit**
- **argparse**
- **urllib3**

These dependencies will be automatically installed if missing when you run the tool.

### External Tools
The following external tools are required for full functionality:
- **Nmap**: For port scanning.
- **Sublist3r**: For subdomain enumeration.
- **wkhtmltopdf**: For generating PDF reports.
- **SQLMap**: For SQL injection testing.

The tool will check if these tools are installed and available in your system's PATH.

---

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/Y518221/HaintSec.git
cd HaintSec
```

### 2. Install Python dependencies:
```bash
pip install -r requirements.txt
pip install .
```

### 3. Ensure the required external tools are installed:
Make sure the following tools are installed and accessible in your system’s PATH:
- **Nmap**: Install using `apt-get install nmap` (Linux) or download from [here](https://nmap.org) for other platforms.
- **Sublist3r**: Install from [Sublist3r GitHub](https://github.com/aboul3la/Sublist3r).
- **wkhtmltopdf**: Install from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html).
- **SQLMap**: Install from [SQLMap GitHub](https://github.com/sqlmapproject/sqlmap).

---

## Usage

To run the **HaintSec** scanner, use the following command:

```bash
haintsec --url <TARGET_URL>
```

### Example:

```bash
haintsec --url https://www.example.com
```
OR 
```bash
python haintsec.py --url https://www.example.com
```
**Arguments:**
- `--url`: The target URL you want to scan (e.g., `https://www.example.com`).

**Note:** Make sure the URL starts with `http://` or `https://`. If the URL doesn't start with either, the script will prepend `https://`.

---

## Configuration

HaintSec uses a **config.json** file for configuration settings. The default configuration is automatically loaded, but you can modify the file to adjust paths and other settings.

### Example **config.json**:
```json
{
    "SQLMAP_PATH": "sqlmap",
    "NMAP_PATH": "/usr/bin/nmap",
    "SUBDOMAIN_TOOL": "sublist3r",
    "WKHTMLTOPDF_TOOL": "/usr/local/bin/wkhtmltopdf",
    "OUTPUT_DIR": "reports",
    "PROXY": null
}
```

### Configuration Fields:
- **SQLMAP_PATH**: Path to the SQLMap tool (default: `sqlmap`).
- **NMAP_PATH**: Path to Nmap (default: detected via system `shutil.which`).
- **SUBDOMAIN_TOOL**: Subdomain enumeration tool (default: `sublist3r`).
- **WKHTMLTOPDF_TOOL**: Path to wkhtmltopdf tool (default: detected via system `shutil.which`).
- **OUTPUT_DIR**: Directory to store the generated reports (default: `reports`).
- **PROXY**: Optional proxy configuration (default: `null`).

---

## Example Outputs

### 1. **Subdomain Enumeration Output**
During subdomain enumeration, **Sublist3r** will identify associated subdomains for the target URL. Here's an example:

```text
[*] Identifying subdomains for https://www.example.com...
[*] Found subdomains:
    - api.example.com
    - blog.example.com
    - mail.example.com
```

### 2. **Vulnerability Scanning Output**
The **vulnerability scan** identifies potential issues like outdated software versions or known CVEs. Example output:

```text
[*] Scanning https://www.example.com for vulnerabilities...
[*] Detected vulnerabilities:
    - XSS Vulnerability (Reflected) on /contact
    - Outdated WordPress version (v5.2) detected
    - Open redirect on /login
```

### 3. **Port Scanning Output**
The **port scan** shows open ports on the target website:

```text
[*] Scanning open ports for https://www.example.com...
[*] Open ports:
    - 80/tcp (HTTP)
    - 443/tcp (HTTPS)
    - 22/tcp (SSH)
```

### 4. **SSL Check Output**
The **SSL check** ensures the SSL certificate is valid:

```text
[*] Checking SSL certificate for https://www.example.com...
[*] SSL Certificate:
    - Issuer: Let's Encrypt
    - Expiration: 2024-05-15
    - Vulnerability: No known vulnerabilities
```

### 5. **SQL Injection Test Output**
The **SQLMap** output identifies potential SQL injection vulnerabilities:

```text
[*] Running SQL injection tests using SQLMap...
[*] SQL Injection detected on /login.php (POST parameter "username")
[*] Test successful: Login bypass achieved.
```

### 6. **Report Generation Output**
After completing the scan, HaintSec generates reports in both DOCX and PDF formats:


### Here’s an example of how the output would look: 

```
===================================================================================================
                                     HaintSec
===================================================================================================
Tool Developed by: Yassine Selmi
GitHub: https://github.com/Y518221
LinkedIn: https://www.linkedin.com/in/yassine-selmi-1ba600260/
===================================================================================================
[*] Checking Python dependencies...
[*] All Python dependencies are satisfied.
[*] Validating configuration...
[*] Configuration is valid.
[*] Missing required tools: Sublist3r
Please install the missing tools and ensure they are available in the PATH.
```

If everything proceeds smoothly and the website https://www.example.com is provided as input and no errors occur, the output of the script would look something like this:

```
===================================================================================================
                                     HaintSec
===================================================================================================
Tool Developed by: Yassine Selmi
GitHub: https://github.com/Y518221
LinkedIn: https://www.linkedin.com/in/yassine-selmi-1ba600260/
===================================================================================================
[*] Checking Python dependencies...
[*] All Python dependencies are satisfied.
[*] Validating configuration...
[*] Configuration is valid.
[*] All required tools are available.
===================================================================================================
Scanning target: https://www.example.com
===================================================================================================
[*] Starting subdomain enumeration...
[*] Found subdomains: api.example.com, blog.example.com (example output)
[*] Subdomain enumeration completed.

[*] Scanning for vulnerabilities...
[*] Vulnerabilities detected:
    - SQL injection in /login
    - XSS in /search (example output)
[*] Vulnerability scanning completed.

[*] Performing port scanning...
[*] Open ports detected: 80 (HTTP), 443 (HTTPS), 22 (SSH) (example output)
[*] Port scanning completed.

[*] Checking SSL/TLS configuration...
[*] SSL/TLS issues:
    - Weak cipher suite detected
    - Expired certificate (example output)
[*] SSL/TLS check completed.

[*] Running SQLMap for advanced scanning...
[*] SQLMap results:
    - Database version: MySQL 5.7
    - Exposed tables: users, orders (example output)
[*] SQLMap scanning completed.

[*] Generating report...
[*] Reports saved as: reports/example_com_report.docx, reports/example_com_report.pdf
[*] Total execution time: 48.67 seconds

```



```text
[*] Reports generated:
    - report.docx
    - report.pdf
```

The generated reports contain detailed findings, including subdomains, vulnerabilities, open ports, SSL information, and SQL injection results.

---

## Logging

HaintSec logs its activities in the **haintsec.log** file. This log includes detailed information about the execution process, including any errors encountered during scanning, tool validation, and dependency installation.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributions

Feel free to fork the repository and submit pull requests for improvements, bug fixes, or new features.

---

## Acknowledgements

- **Nmap**: [https://nmap.org](https://nmap.org)
- **Sublist3r**: [https://github.com/aboul3la/Sublist3r](https://github.com/aboul3la/Sublist3r)
- **wkhtmltopdf**: [https://wkhtmltopdf.org](https://wkhtmltopdf.org)
- **SQLMap**: [https://github.com/sqlmapproject/sqlmap](https://github.com/sqlmapproject/sqlmap)
