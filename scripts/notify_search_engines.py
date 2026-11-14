#!/usr/bin/env python3
"""
Final Third — Automated Search Engine Indexing & Instant Notification Engine
Supports:
1. IndexNow Protocol (Instant submission to Microsoft Bing, Yandex, Seznam, Naver & aggregators)
   - Key: 9f4c3a287e1b4b5ea3c7198d02e482bb
   - Key verification: https://www.finalthird-haris.com/9f4c3a287e1b4b5ea3c7198d02e482bb.txt
2. Google & Bing XML Sitemap & RSS Feed pings
3. Google Indexing API (Direct push notifications for immediate crawling queue)
   - Reads GOOGLE_INDEXING_CREDENTIALS or INDEXING_SERVICE_ACCOUNT_JSON if configured.
4. Executes automatically during daily sync workflows or on-demand.
"""

import os
import sys
import json
import ssl
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITEMAP_PATH = os.path.join(BASE_DIR, "sitemap.xml")
INDEXNOW_KEY = "9f4c3a287e1b4b5ea3c7198d02e482bb"
HOST = "www.finalthird-haris.com"
KEY_LOCATION = f"https://{HOST}/{INDEXNOW_KEY}.txt"
SITEMAP_URL = f"https://{HOST}/sitemap.xml"
FEED_URL = f"https://{HOST}/feed.xml"

def safe_request(url, data=None, headers=None, method=None, timeout=15):
    """Robust HTTP request wrapper with SSL verification fallback."""
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; FinalThirdIndexingEngine/1.0; +https://www.finalthird-haris.com)"
        }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.getcode(), response.read().decode("utf-8", errors="ignore")
    except (ssl.SSLError, urllib.error.URLError) as e:
        if isinstance(e, ssl.SSLError) or (isinstance(e, urllib.error.URLError) and "CERTIFICATE_VERIFY_FAILED" in str(e)):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            try:
                with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
                    return response.getcode(), response.read().decode("utf-8", errors="ignore")
            except urllib.error.HTTPError as he:
                return he.code, he.read().decode("utf-8", errors="ignore")
            except Exception as ex:
                return 0, str(ex)
        if isinstance(e, urllib.error.HTTPError):
            return e.code, e.read().decode("utf-8", errors="ignore")
        return 0, str(e)
    except urllib.error.HTTPError as he:
        return he.code, he.read().decode("utf-8", errors="ignore")
    except Exception as ex:
        return 0, str(ex)

def get_all_sitemap_urls():
    """Extracts all canonical URLs from sitemap.xml."""
    urls = []
    if os.path.exists(SITEMAP_PATH):
        try:
            tree = ET.parse(SITEMAP_PATH)
            root = tree.getroot()
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            for loc in root.findall(".//s:loc", ns):
                if loc.text and loc.text.strip():
                    urls.append(loc.text.strip())
        except Exception as e:
            print(f"[Warning] Error parsing sitemap.xml: {e}")

    # Fallback to standard core pages if sitemap parsing failed
    if not urls:
        urls = [
            f"https://{HOST}/",
            f"https://{HOST}/football/",
            f"https://{HOST}/cricket/",
            f"https://{HOST}/about.html",
            f"https://{HOST}/contact.html",
            f"https://{HOST}/privacy.html",
            f"https://{HOST}/terms.html"
        ]

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            deduped.append(u)
    return deduped

def submit_indexnow(urls):
    """
    Submits URLs to the IndexNow protocol (used by Bing, Yandex, Seznam, Naver).
    Documentation: https://www.indexnow.org/documentation
    """
    if not urls:
        return {"status": "skipped", "message": "No URLs provided"}

    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls[:10000] # IndexNow allows up to 10,000 URLs per call
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "FinalThird-IndexNow/1.0 (+https://www.finalthird-haris.com)"
    }

    results = {}
    endpoints = [
        ("IndexNow Central (api.indexnow.org)", "https://api.indexnow.org/indexnow"),
        ("Microsoft Bing (bing.com)", "https://www.bing.com/indexnow")
    ]

    for name, endpoint in endpoints:
        code, body = safe_request(endpoint, data=data, headers=headers, method="POST")
        # 200 = OK, 202 = Accepted
        success = code in (200, 202)
        results[name] = {
            "status_code": code,
            "success": success,
            "response": body[:200]
        }
        status_sym = "✓" if success else "✗"
        print(f"[{status_sym}] {name}: HTTP {code} (Submitted {len(urls)} URLs)")

    return results

def ping_search_engines():
    """
    Pings search engine sitemap notification endpoints.
    """
    results = {}
    ping_targets = [
        ("Google Sitemap Ping", f"https://www.google.com/ping?sitemap={SITEMAP_URL}"),
        ("Bing Sitemap Ping", f"https://www.bing.com/ping?sitemap={SITEMAP_URL}")
    ]

    for name, url in ping_targets:
        code, body = safe_request(url, method="GET")
        success = code in (200, 202)
        results[name] = {
            "status_code": code,
            "success": success
        }
        status_sym = "✓" if success else "ℹ"
        print(f"[{status_sym}] {name}: HTTP {code}")

    return results

def submit_google_indexing_api(urls):
    """
    Submits URLs directly to the Google Indexing API if service account credentials are available.
    Requires Google Cloud Service Account with Search Console ownership.
    """
    creds_json = (
        os.environ.get("GOOGLE_INDEXING_CREDENTIALS") or
        os.environ.get("INDEXING_SERVICE_ACCOUNT_JSON") or
        ""
    )
    creds_file = os.path.join(BASE_DIR, "service_account.json")
    if not creds_json and os.path.exists(creds_file):
        try:
            with open(creds_file, "r") as f:
                creds_json = f.read()
        except Exception:
            pass

    if not creds_json:
        print("[ℹ Info] Google Indexing API: No Service Account credentials configured.")
        print("        IndexNow (Bing, Yandex) and Google sitemap/feed indexing are active.")
        print("        To enable direct Google API push indexing, set INDEXING_SERVICE_ACCOUNT_JSON in GitHub Secrets.")
        return {"status": "unconfigured", "count": 0}

    try:
        # Check if google-auth is available
        from google.oauth2 import service_account
        import google.auth.transport.requests

        service_info = json.loads(creds_json) if isinstance(creds_json, str) and creds_json.strip().startswith("{") else json.load(open(creds_json))
        SCOPES = ["https://www.googleapis.com/auth/indexing"]
        credentials = service_account.Credentials.from_service_account_info(service_info, scopes=SCOPES)
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        access_token = credentials.token

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {access_token}"
        }

        submitted = 0
        endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"

        # Prioritize homepage, category hubs, and newest video pages (up to daily quota)
        target_urls = urls[:50]
        for url in target_urls:
            payload = json.dumps({"url": url, "type": "URL_UPDATED"}).encode("utf-8")
            code, resp = safe_request(endpoint, data=payload, headers=headers, method="POST")
            if code in (200, 202):
                submitted += 1
            time.sleep(0.1) # Respect Google Indexing API rate limits

        print(f"[✓] Google Indexing API: Successfully submitted {submitted}/{len(target_urls)} URLs to Google crawl queue.")
        return {"status": "success", "count": submitted}

    except Exception as e:
        print(f"[Warning] Google Indexing API submission encountered an error: {e}")
        return {"status": "error", "error": str(e)}

def notify_all(urls=None, dry_run=False):
    """
    Main entry point: Submits all site URLs across all automated indexing channels.
    """
    print("=" * 70)
    print("FINAL THIRD — AUTOMATED DAILY SEARCH ENGINE INDEXING")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    if urls is None:
        urls = get_all_sitemap_urls()

    print(f"Total discovered pages for daily indexing: {len(urls)}")
    print(f"Domain: https://{HOST}")
    print(f"IndexNow Key: {INDEXNOW_KEY} (served at {KEY_LOCATION})")

    if dry_run:
        print("[DRY RUN] Skipping network calls to search engine indexing endpoints.")
        return {"dry_run": True, "url_count": len(urls)}

    print("\n--- 1. IndexNow Protocol (Bing, Yandex, Seznam, Naver) ---")
    indexnow_res = submit_indexnow(urls)

    print("\n--- 2. Search Engine Sitemap Pings ---")
    ping_res = ping_search_engines()

    print("\n--- 3. Google Indexing API (Direct Push) ---")
    google_res = submit_google_indexing_api(urls)

    print("\n" + "=" * 70)
    print("✓ Daily search engine indexing submissions finished.")
    print("=" * 70)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "url_count": len(urls),
        "indexnow": indexnow_res,
        "pings": ping_res,
        "google_indexing_api": google_res
    }

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    notify_all(dry_run=is_dry)
