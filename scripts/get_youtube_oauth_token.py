#!/usr/bin/env python3
"""
Final Third — YouTube OAuth 2.0 Refresh Token Generator
Helper script for channel owner (Haris Nenmara).

Usage:
  python3 scripts/get_youtube_oauth_token.py

What it does:
1. Prompts for your Google Cloud OAuth Client ID and Client Secret.
2. Generates an authorization URL for the required YouTube scope:
   https://www.googleapis.com/auth/youtube.force-ssl
3. Launches a local web server (http://localhost:8080) to capture the callback.
4. Exchanges the one-time code for a long-lived REFRESH_TOKEN.
5. Displays the exact values to add to GitHub Repository Secrets.
"""

import sys
import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser

AUTH_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
REDIRECT_URI = "http://localhost:8080"
auth_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body style="font-family:sans-serif; text-align:center; padding:50px; background:#080808; color:#9EE20B;">
                    <h1>&#10003; Authorization Successful!</h1>
                    <p style="color:#fff;">You can close this tab and return to your terminal.</p>
                </body>
                </html>
            """)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Failed to capture authorization code.")
            
    def log_message(self, format, *args):
        return  # Silence server logs

def main():
    print("=" * 80)
    print("FINAL THIRD — YOUTUBE OAUTH 2.0 REFRESH TOKEN GENERATOR")
    print("=" * 80)
    print("This script helps Haris Nenmara obtain the OAuth Refresh Token required")
    print("for YouTube Data API v3 captions.download access.\n")

    client_id = input("Enter your OAuth Client ID: ").strip()
    client_secret = input("Enter your OAuth Client Secret: ").strip()

    if not client_id or not client_secret:
        print("\nError: Client ID and Client Secret are required.")
        sys.exit(1)

    auth_params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": AUTH_SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(auth_params)

    print("\nOpening Google login & consent page in your default browser...")
    print("If your browser doesn't open automatically, visit this URL:\n")
    print(auth_url)
    print("\nWaiting for authorization callback on http://localhost:8080 ...")

    webbrowser.open(auth_url)

    server = HTTPServer(("localhost", 8080), OAuthHandler)
    while auth_code is None:
        server.handle_request()

    print("\n✓ Authorization code received!")
    print("Exchanging authorization code for OAuth Refresh Token...")

    token_url = "https://oauth2.googleapis.com/token"
    token_params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }
    data = urllib.parse.urlencode(token_params).encode("utf-8")
    req = urllib.request.Request(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            token_data = json.loads(resp.read().decode("utf-8"))
            refresh_token = token_data.get("refresh_token")
            access_token = token_data.get("access_token")

            if not refresh_token:
                print("\n[Notice] No refresh token returned. Did you already authorize this app?")
                print("Try running again with prompt='consent' or revoke access at https://myaccount.google.com/permissions")
                print("Access token:", access_token[:15] + "...")
                return

            print("\n" + "=" * 80)
            print("SUCCESS! CONFIGURE THESE SECRETS IN GITHUB REPOSITORY SETTINGS:")
            print("=" * 80)
            print(f"YOUTUBE_CLIENT_ID:      {client_id}")
            print(f"YOUTUBE_CLIENT_SECRET:  {client_secret}")
            print(f"YOUTUBE_REFRESH_TOKEN:  {refresh_token}")
            print("=" * 80)
            print("\nTo add these to GitHub:")
            print("1. Go to your GitHub repo -> Settings -> Secrets and variables -> Actions")
            print("2. Click 'New repository secret'")
            print("3. Add YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN.")
            print("✓ Daily YouTube Caption Sync will now run automatically via GitHub Actions!\n")

    except urllib.error.HTTPError as e:
        print(f"\n[Error] Token exchange failed: {e.code} {e.reason}")
        print(e.read().decode("utf-8"))
    except Exception as e:
        print(f"\n[Error] Unexpected error: {e}")

if __name__ == "__main__":
    main()
