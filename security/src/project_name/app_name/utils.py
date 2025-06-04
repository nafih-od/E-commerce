import subprocess
import socket
import ssl
#import nmap
import dns.resolver
from datetime import datetime
import requests
import time
import subprocess


def ping(host):
    print(f"\n🛰️ Pinging {host}")
    try:
        output = subprocess.check_output(["ping",host], stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print(f"Ping failed:\n{e.output.decode()}")


def ssl_info(domain):
    print(f"\n🔐 SSL Info for {domain}")
    ctx = ssl.create_default_context()
    try:
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()
            print(f"Issuer: {cert['issuer']}")
            print(f"Valid From: {cert['notBefore']}")
            print(f"Valid Until: {cert['notAfter']}")
            expire_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            days_left = (expire_date - datetime.utcnow()).days
            print(f"Days until expiration: {days_left}")
    except Exception as e:
        print(f"SSL Check failed: {e}")


def check_http_security_headers(domain):
    print(f"\n🛡️ HTTP Security Headers for {domain}")
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        headers = response.headers

        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Referrer-Policy",
            "Permissions-Policy",
        ]

        for header in security_headers:
            value = headers.get(header, "❌ Not Set")
            print(f"{header}: {value}")
    except Exception as e:
        print(f"Failed to fetch headers: {e}")


def check_ssllabs(domain):
    print(f"\n📊 SSL Labs Grade for {domain}")
    api_url = "https://api.ssllabs.com/api/v3/analyze"

    try:
        params = {"host": domain, "publish": "off", "startNew": "on", "all": "done"}
        print("Requesting analysis from SSL Labs (may take up to 2-3 mins)...")

        # Start analysis
        response = requests.get(api_url, params=params, timeout=10)
        analysis = response.json()

        # Poll until it's ready
        while analysis.get("status") in ["DNS", "IN_PROGRESS", "INITIALIZING"]:
            print(f"Status: {analysis['status']}... waiting...")
            time.sleep(10)
            response = requests.get(api_url, params={"host": domain})
            analysis = response.json()

        # Once ready
        if analysis.get("status") == "READY":
            endpoint = analysis["endpoints"][0]
            grade = endpoint.get("grade", "N/A")
            print(f"SSL Labs Grade: {grade}")
            print(f"IP Address: {endpoint.get('ipAddress')}")
            print(f"Supports TLS: {endpoint.get('details', {}).get('protocols', [])}")
        else:
            print(f"Scan failed or blocked: {analysis.get('status')}")

    except Exception as e:
        print(f"SSL Labs check failed: {e}")


def detect_cms_with_whatweb(domain):
    print(f"\n🧠 CMS & Technology Fingerprinting for {domain} using WhatWeb")
    try:
        result = subprocess.run(
            ["whatweb", domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"Error: {result.stderr.strip()}")
    except FileNotFoundError:
        print("❌ WhatWeb is not installed or not found in PATH.")
    except subprocess.TimeoutExpired:
        print("❌ WhatWeb scan timed out.")


def ns_lookup(domain):
    print(f"\n🔍 NSLookup for {domain}")
    try:
        result = dns.resolver.resolve(domain, 'A')
        for ip in result:
            print(f"A Record: {ip}")
    except Exception as e:
        print(f"NSLookup failed: {e}")



def detect_waf_and_cloudflare(domain):
    print(f"\n🛡️ WAF / CDN / Cloudflare Detection for {domain}")
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        headers = response.headers

        indicators = {
            "cloudflare": ["cf-ray", "cf-cache-status", "server: cloudflare"],
            "sucuri": ["x-sucuri-id", "x-sucuri-cache"],
            "akamai": ["x-akamai-transformed"],
            "imperva": ["x-cdn", "x-iinfo"],
        }

        found = []

        for vendor, signs in indicators.items():
            for key in signs:
                for header_key in headers:
                    if key.lower() in header_key.lower() or key.lower() in str(headers.get(header_key, "")).lower():
                        found.append(vendor)
                        break

        if found:
            print(f"Detected WAF/CDN: {', '.join(set(found)).title()}")
        else:
            print("❌ No obvious WAF/CDN detected.")

        # Optional: DNS check for cloudflare
        try:
            cname = dns.resolver.resolve(domain, 'CNAME')
            for r in cname:
                if "cloudflare" in str(r).lower():
                    print("✅ Cloudflare CNAME detected in DNS.")
        except:
            pass

    except Exception as e:
        print(f"WAF/CDN check failed: {e}")


def cve_lookup_tech(tech_name):
    print(f"\n🔎 Searching for CVEs related to: {tech_name}")
    try:
        # Basic online CVE scraping from cvedetails.com
        search_url = f"https://www.cvedetails.com/google-search-results.php?q={tech_name.replace(' ', '+')}"
        response = requests.get(search_url, timeout=10)
        if "CVE" in response.text:
            print(f"✅ Potential CVEs found. Visit: {search_url}")
        else:
            print("❌ No CVEs found (or not indexed). Try manually.")
    except Exception as e:
        print(f"CVE lookup failed: {e}")













