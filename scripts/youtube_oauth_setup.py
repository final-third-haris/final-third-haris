#!/usr/bin/env python3
"""
Final Third — YouTube OAuth Setup & Secure Refresh Token Generator
Author: Final Third Engineering
Purpose:
Interactive, secure tool for channel owner (Haris Nenmara) to authorize
YouTube Data API v3 and generate a long-lived Refresh Token for automated
closed caption track downloading.

Security:
- Never prints unmasked secret values to stdout or logs.
- Saves tokens exclusively to .credentials.json (which is gitignored).
- Verifies the authorized channel matches channel ID: UClD0Kli5qi5JE2tI1ReHLLQ.
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

REQUIRED_CHANNEL_ID = "UClD0Kli5qi5JE2tI1ReHLLQ"
OAUTH_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
TOKEN_URL = "https://oauth2.googleapis.com/token"
CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true"

def mask(val):
    if not val or len(val) < 8:
        return "****"
    return f"{val[:4]}...{val[-4:]}"

def exchange_code(client_id, client_secret, auth_code, redirect_uri):
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(
        TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error exchanging authorization code: {e}")
        return None

def verify_channel(access_token):
    req = urllib.request.Request(
        CHANNELS_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("items", [])
            if items:
                ch = items[0]
                ch_id = ch.get("id")
                ch_title = ch.get("snippet", {}).get("title")
                return ch_id, ch_title
    except Exception as e:
        print(f"Notice: Channel verification call returned: {e}")
    return None, None

def main():
    print("=" * 70)
    print("FINAL THIRD — YOUTUBE OAUTH 2.0 REFRESH TOKEN GENERATOR")
    print("=" * 70)
    print("This script helps Haris authorize the @FinalThird_HarisNenmara channel")
    print("so the automated sync can download Malayalam captions.\n")

    client_id = os.environ.get("YOUTUBE_CLIENT_ID", "").strip()
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET", "").strip()

    if not client_id:
        client_id = input("Enter your Google Cloud OAuth Client ID: ").strip()
    if not client_secret:
        client_secret = input("Enter your Google Cloud OAuth Client Secret: ").strip()

    if not (client_id and client_secret):
        print("Error: Client ID and Client Secret are required.")
        sys.exit(1)

    port = 8085
    redirect_uri = f"http://localhost:{port}/"

    auth_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": OAUTH_SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(auth_params)}"

    print("\nStep 1: Open the following URL in your browser and sign in with")
    print("the Google account that manages @FinalThird_HarisNenmara:\n")
    print(auth_url)
    print("\nWaiting for authorization response on localhost...")

    auth_code = None

    class OAuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal auth_code
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            if "code" in query:
                auth_code = query["code"][0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<h1>Authorization Successful!</h1><p>You can close this tab and return to the terminal.</p>")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"<h1>Authorization Failed</h1><p>No authorization code received.</p>")

        def log_message(self, format, *args):
            pass

    server = HTTPServer(("localhost", port), OAuthHandler)
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    while not auth_code:
        server.handle_request()

    server.server_close()

    print("\nStep 2: Exchanging authorization code for refresh token...")
    token_resp = exchange_code(client_id, client_secret, auth_code, redirect_uri)
    if not token_resp or "refresh_token" not in token_resp:
        print("\n[ERROR] Failed to obtain refresh token.")
        if token_resp and "error" in token_resp:
            print(f"OAuth Error: {token_resp.get('error')} — {token_resp.get('error_description')}")
        sys.exit(1)

    refresh_token = token_resp["refresh_token"]
    access_token = token_resp.get("access_token")

    print("\nStep 3: Verifying authorized channel...")
    ch_id, ch_title = verify_channel(access_token)
    if ch_id:
        print(f"✓ Authorized Channel: '{ch_title}' (Channel ID: {ch_id})")
        if ch_id == REQUIRED_CHANNEL_ID:
            print("✓ Matches required Final Third channel ID perfectly!")
        else:
            print(f"[Warning] Authorized channel ID {ch_id} does not match {REQUIRED_CHANNEL_ID}.")
    else:
        print("Note: Channel details could not be verified online (token generated).")

    # Save to local gitignored file
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cred_path = os.path.join(base_dir, ".credentials.json")
    with open(cred_path, "w", encoding="utf-8") as f:
        json.dump({
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token
        }, f, indent=2)

    print(f"\n✓ Saved credentials locally to gitignored file: {cred_path}")
    print("\n" + "=" * 70)
    print("NEXT ACTIONS IN GITHUB REPOSITORY SETTINGS:")
    print("=" * 70)
    print("Go to your GitHub repository -> Settings -> Secrets and variables -> Actions")
    print("Create the following three repository secrets:\n")
    print(f"1. YOUTUBE_CLIENT_ID     : [Configured: {mask(client_id)}]")
    print(f"2. YOUTUBE_CLIENT_SECRET : [Configured: {mask(client_secret)}]")
    print(f"3. YOUTUBE_REFRESH_TOKEN : [Configured: {mask(refresh_token)}]")
    print("\n(Actual values were saved to .credentials.json and never logged.)")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
