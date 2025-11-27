"""
Helper script to set up Gmail authentication
"""
import asyncio
import sys
from services.gmail_service import GmailService

async def setup_gmail():
    """Interactive Gmail setup"""
    print("=" * 60)
    print("Gmail Authentication Setup")
    print("=" * 60)
    print()
    
    gmail_service = GmailService()
    
    # Check if already authenticated
    if await gmail_service.is_authenticated():
        print("[OK] Gmail is already authenticated!")
        response = input("Do you want to re-authenticate? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Get authorization URL
    try:
        print("\n1. Getting authorization URL...")
        auth_url = await gmail_service.get_authorization_url()
        print(f"\n[OK] Authorization URL generated!")
        print(f"\nPlease visit this URL in your browser:")
        print(f"\n{auth_url}\n")
        print("After authorizing, you'll receive an authorization code.")
        print("Copy that code and paste it below.\n")
        
        # Get authorization code
        code = input("Enter the authorization code: ").strip()
        
        if not code:
            print("No code provided. Setup cancelled.")
            return
        
        # Handle callback
        print("\n2. Processing authorization code...")
        await gmail_service.handle_oauth_callback(code)
        
        print("\n[OK] Gmail authentication successful!")
        print("You can now use the Gmail API endpoints.")
        
    except FileNotFoundError:
        print("\n[ERROR] credentials.json not found!")
        print("\nPlease:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create/select a project")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download and save as 'credentials.json' in this directory")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(setup_gmail())

