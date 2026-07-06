"""
One-time Gmail OAuth setup.
Run: python setup_gmail.py
Opens browser for Google login, saves token.json for email monitoring.
"""
import os
import sys
from dotenv import load_dotenv
load_dotenv(override=True)

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
TOKEN_PATH = "token.json"

def main():
    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")

    if not client_id or not client_secret or client_id == "your_gmail_client_id":
        print("ERROR: GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET must be set in .env")
        sys.exit(1)

    if os.path.exists(TOKEN_PATH):
        print("token.json already exists. Delete it to re-authenticate.")
        sys.exit(0)

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    print("Opening browser for Google OAuth login...")
    print("After authorizing, you'll be redirected to localhost — that's normal.")
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=8090)

    with open(TOKEN_PATH, 'w') as token:
        token.write(creds.to_json())

    print(f"SUCCESS: token.json saved. Email monitoring is now enabled.")

if __name__ == "__main__":
    main()
