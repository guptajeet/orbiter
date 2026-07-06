import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
TOKEN_PATH = "token.json"

class OAuthManager:
    @staticmethod
    def get_gmail_credentials():
        creds = None
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                client_id = os.getenv("GMAIL_CLIENT_ID")
                client_secret = os.getenv("GMAIL_CLIENT_SECRET")

                if not client_id or not client_secret:
                    raise Exception("Missing GMAIL_CLIENT_ID or GMAIL_CLIENT_SECRET in .env")

                client_config = {
                    "installed": {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": ["http://localhost"],
                    }
                }
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())

        return creds

oauth_manager = OAuthManager()
