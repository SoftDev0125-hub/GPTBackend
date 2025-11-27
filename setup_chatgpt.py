"""
Helper script to set up ChatGPT integration
"""
import os
import json
import requests
from pathlib import Path

def check_ngrok():
    """Check if ngrok is available"""
    import subprocess
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] ngrok is installed")
            print(f"   {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("[INFO] ngrok is not installed")
        print("   Install from: https://ngrok.com/download")
        return False
    return False

def get_openapi_schema(base_url="http://localhost:8000"):
    """Download OpenAPI schema"""
    try:
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            schema = response.json()
            # Save to file
            with open("openapi_schema.json", "w") as f:
                json.dump(schema, f, indent=2)
            print(f"[OK] OpenAPI schema downloaded and saved to openapi_schema.json")
            print(f"   Title: {schema.get('info', {}).get('title', 'Unknown')}")
            print(f"   Endpoints: {len(schema.get('paths', {}))}")
            return True
        else:
            print(f"[ERROR] Failed to download schema: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to download schema: {e}")
        return False

def create_assistant_instructions():
    """Create assistant instructions file"""
    instructions = """You are a helpful assistant that can:
- Read and manage Gmail messages
- Send emails on behalf of the user
- Reply to emails
- Start and stop applications on the user's computer

When the user asks you to:
- Send an email: Use the /gmail/send endpoint
- Read emails: Use the /gmail/messages endpoint
- Reply to an email: Use the /gmail/reply endpoint
- Start an app: Use the /apps/control endpoint with action="start"
- Stop an app: Use the /apps/control endpoint with action="stop"

Always be helpful and confirm actions before executing them.
When sending emails, use a friendly and professional tone.
When the user says "send 'hi' to abel", send an email to abel@example.com (or extract the email from context) with the message "hi".
"""
    
    with open("assistant_instructions.txt", "w") as f:
        f.write(instructions)
    print("[OK] Assistant instructions saved to assistant_instructions.txt")
    return instructions

def main():
    print("=" * 60)
    print("ChatGPT Integration Setup")
    print("=" * 60)
    print()
    
    # Step 1: Check server
    print("Step 1: Checking server...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("[OK] Server is running at http://localhost:8000")
        else:
            print("[WARNING] Server responded with status:", response.status_code)
    except Exception as e:
        print(f"[ERROR] Server is not accessible: {e}")
        print("   Please start the server: python run.py")
        return
    
    print()
    
    # Step 2: Check ngrok
    print("Step 2: Checking ngrok...")
    has_ngrok = check_ngrok()
    print()
    
    # Step 3: Download OpenAPI schema
    print("Step 3: Downloading OpenAPI schema...")
    base_url = "http://localhost:8000"
    if has_ngrok:
        ngrok_url = input("Enter your ngrok URL (or press Enter to use localhost): ").strip()
        if ngrok_url:
            base_url = ngrok_url.rstrip('/')
    
    get_openapi_schema(base_url)
    print()
    
    # Step 4: Create instructions
    print("Step 4: Creating assistant instructions...")
    create_assistant_instructions()
    print()
    
    # Summary
    print("=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print()
    print("1. Make your API publicly accessible:")
    if has_ngrok:
        print("   Run: ngrok http 8000")
        print("   Copy the HTTPS URL (e.g., https://abc123.ngrok.io)")
    else:
        print("   Option A: Install ngrok and run: ngrok http 8000")
        print("   Option B: Deploy to a cloud service (Heroku, Railway, etc.)")
    print()
    print("2. Create OpenAI Assistant:")
    print("   - Go to https://platform.openai.com/assistants")
    print("   - Click 'Create Assistant'")
    print("   - In 'Actions', click 'Add Action'")
    print("   - Select 'Import from URL' or 'Import from File'")
    print("   - Use your public URL: https://your-url.ngrok.io/openapi.json")
    print("     OR upload: openapi_schema.json")
    print("   - Copy instructions from: assistant_instructions.txt")
    print()
    print("3. Test the integration:")
    print("   - Send a message: 'Send hi to abel@example.com'")
    print("   - ChatGPT will call your API automatically!")
    print()
    print("Files created:")
    print("  - openapi_schema.json (OpenAPI schema)")
    print("  - assistant_instructions.txt (Assistant instructions)")

if __name__ == "__main__":
    main()

