"""
Helper script to complete Gmail authentication
Usage: python complete_gmail_auth.py YOUR_AUTH_CODE
"""
import asyncio
import sys
import requests

async def complete_auth(code: str):
    """Complete Gmail authentication with the provided code"""
    try:
        response = requests.post(
            f"http://localhost:8000/gmail/auth/callback",
            params={"code": code}
        )
        
        if response.status_code == 200:
            print("[OK] Gmail authentication successful!")
            print("You can now use the Gmail API endpoints.")
            return True
        else:
            print(f"[ERROR] Authentication failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python complete_gmail_auth.py YOUR_AUTH_CODE")
        print("\nTo get the authorization URL, visit: http://localhost:8000/gmail/auth/url")
        sys.exit(1)
    
    code = sys.argv[1]
    asyncio.run(complete_auth(code))

