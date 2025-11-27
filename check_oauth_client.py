"""
Check OAuth client type and provide setup instructions
"""
import json
import os

def check_client_type():
    """Check the OAuth client type from credentials.json"""
    credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
    
    if not os.path.exists(credentials_path):
        print("[ERROR] credentials.json not found!")
        print("\nPlease download OAuth 2.0 credentials from Google Cloud Console.")
        return None
    
    try:
        with open(credentials_path, 'r') as f:
            creds_data = json.load(f)
        
        if 'installed' in creds_data:
            print("[OK] Desktop/Installed App OAuth client detected")
            print("This client type should work with the current setup.")
            return 'installed'
        elif 'web' in creds_data:
            print("[INFO] Web Application OAuth client detected")
            print("\nYou have two options:")
            print("\nOption 1: Create a Desktop App client (Recommended)")
            print("  1. Go to https://console.cloud.google.com/apis/credentials")
            print("  2. Create Credentials > OAuth client ID")
            print("  3. Select 'Desktop app'")
            print("  4. Download and replace credentials.json")
            print("\nOption 2: Configure Web client redirect URI")
            print("  1. Go to https://console.cloud.google.com/apis/credentials")
            print("  2. Click on your OAuth 2.0 Client ID")
            print("  3. Add 'http://localhost:8000/oauth2callback' to Authorized redirect URIs")
            print("  4. Save and try again")
            return 'web'
        else:
            print("[WARNING] Unknown client type")
            return None
    except Exception as e:
        print(f"[ERROR] Failed to read credentials: {e}")
        return None

if __name__ == "__main__":
    check_client_type()

