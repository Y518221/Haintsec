from docx import Document
import pdfkit
from datetime import datetime

def generate_report(url, subdomains, vulnerabilities, open_ports, ssl_issues):
    domain = url.replace("https://", "").replace("http://", "").replace("/", "")

    # Add timestamp to the file name to prevent overwriting
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    REPORT_OUTPUT_DOCX = f"{domain}_vulnerability_report_{timestamp}.docx"
    REPORT_OUTPUT_PDF = f"{domain}_vulnerability_report_{timestamp}.pdf"

    # Create a new Document
    doc = Document()
    doc.add_heading(f"Vulnerability Report for {domain}", 0)

    # Subdomains Section
    doc.add_heading("Subdomains Identified", level=1)
    if subdomains:
        doc.add_paragraph("\n".join(subdomains))
    else:
        doc.add_paragraph("No subdomains found.")
        doc.add_paragraph("[!] Actionable Insight: Consider performing subdomain enumeration to uncover potential attack vectors.")

    # Vulnerabilities Section
    doc.add_heading("Vulnerabilities Found", level=1)
    if vulnerabilities:
        for vuln in vulnerabilities:
            doc.add_paragraph(f"Type: {vuln['type']}\nDetail: {vuln['detail']}")
    else:
        doc.add_paragraph("No vulnerabilities found.")
        doc.add_paragraph("[!] Actionable Insight: Review the website for missing input validation, unprotected forms, etc.")

    # Open Ports Section
    doc.add_heading("Open Ports", level=1)
    if open_ports:
        for host, ports in open_ports.items():
            doc.add_paragraph(f"{host}: {ports}")
    else:
        doc.add_paragraph("No open ports found.")
        doc.add_paragraph("[!] Actionable Insight: Conduct a port scan using Nmap to uncover any exposed services.")

    # SSL/TLS Issues Section
    doc.add_heading("SSL Issues", level=1)
    if ssl_issues:
        for issue in ssl_issues:
            doc.add_paragraph(issue)
    else:
        doc.add_paragraph("No SSL/TLS issues found.")
        doc.add_paragraph("[!] Actionable Insight: Ensure SSL/TLS configurations are correctly implemented and up to date.")

    # Save the DOCX file
    doc.save(REPORT_OUTPUT_DOCX)

    # Convert DOCX to PDF using pdfkit
    try:
        pdfkit.from_file(REPORT_OUTPUT_DOCX, REPORT_OUTPUT_PDF)
    except Exception as e:
        print(f"[!] Error generating PDF: {e}")

    return REPORT_OUTPUT_DOCX, REPORT_OUTPUT_PDF
