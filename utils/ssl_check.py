import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime, timezone

def check_ssl(url):
    """Check the SSL/TLS configuration for a given URL."""
    domain = urlparse(url).netloc
    ssl_issues = []

    try:
        # Create SSL context and try to establish a connection
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
        conn.settimeout(10)
        conn.connect((domain, 443))
        cert = conn.getpeercert()

        # Check if certificate exists
        if not cert:
            ssl_issues.append("Certificate is invalid or not found.")
        else:
            # Extract the certificate expiration date
            not_after = cert.get('notAfter')
            cert_expiration = datetime.strptime(not_after, '%b %d %H:%M:%S %Y GMT')

            # Convert the cert expiration time to a timezone-aware datetime
            cert_expiration = cert_expiration.replace(tzinfo=timezone.utc)

            # Get the current time in UTC (timezone-aware)
            current_time = datetime.now(timezone.utc)

            # Check if the certificate is expired
            if cert_expiration < current_time:
                ssl_issues.append("Certificate is expired.")
            
            # Check if the certificate is self-signed (issuer and subject are the same)
            if cert['issuer'] == cert['subject']:
                ssl_issues.append("Self-signed certificate detected.")
    
    except ssl.SSLError as e:
        # SSL specific errors
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            ssl_issues.append("Certificate verification failed. The certificate may be expired or invalid.")
        elif "self-signed certificate" in str(e):
            ssl_issues.append("Self-signed certificate detected.")
        else:
            ssl_issues.append(f"SSL/TLS error: {e}")
    except socket.timeout:
        ssl_issues.append(f"Timeout occurred while trying to connect to {domain}.")
    except Exception as e:
        ssl_issues.append(f"Error checking SSL/TLS: {e}")

    return ssl_issues
