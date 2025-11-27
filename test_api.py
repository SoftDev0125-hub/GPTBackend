"""
Quick test script for API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_gmail_auth_status():
    """Test Gmail auth status"""
    print("Testing /gmail/auth/status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/gmail/auth/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        return response.json().get("authenticated", False)
    except Exception as e:
        print(f"Error: {e}\n")
        return False

def test_list_apps():
    """Test list apps endpoint"""
    print("Testing /apps/list endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/apps/list")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Available apps: {len(data.get('apps', []))}")
        for app in data.get('apps', []):
            status = "Running" if app.get('running') else "Stopped"
            print(f"  - {app.get('name')}: {status}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}\n")
        return False

def test_send_email(to_email, subject, body):
    """Test send email endpoint"""
    print(f"Testing /gmail/send endpoint...")
    print(f"Sending email to: {to_email}")
    try:
        response = requests.post(
            f"{BASE_URL}/gmail/send",
            json={
                "to": to_email,
                "subject": subject,
                "body": body
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}\n")
        return False

def test_get_messages(max_results=5):
    """Test get messages endpoint"""
    print(f"Testing /gmail/messages endpoint (max_results={max_results})...")
    try:
        response = requests.get(
            f"{BASE_URL}/gmail/messages",
            params={"max_results": max_results}
        )
        print(f"Status: {response.status_code}")
        messages = response.json()
        print(f"Found {len(messages)} messages")
        for msg in messages[:3]:  # Show first 3
            from_email = msg.get('from_email', 'Unknown')
            subject = msg.get('subject', 'No Subject')
            snippet = msg.get('snippet', '')[:50]
            # Handle encoding issues
            try:
                print(f"  - From: {from_email}")
                print(f"    Subject: {subject}")
                print(f"    Snippet: {snippet}...")
            except UnicodeEncodeError:
                print(f"  - From: {from_email.encode('ascii', 'ignore').decode()}")
                print(f"    Subject: {subject.encode('ascii', 'ignore').decode()}")
                print(f"    Snippet: {snippet.encode('ascii', 'ignore').decode()}...")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}\n")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("API Endpoint Tests")
    print("=" * 60)
    print()
    
    # Basic health check
    if not test_health():
        print("Server is not running or not accessible!")
        exit(1)
    
    # Gmail auth status
    is_authenticated = test_gmail_auth_status()
    
    # List apps
    test_list_apps()
    
    # Gmail tests (only if authenticated)
    if is_authenticated:
        print("Gmail is authenticated. Testing Gmail endpoints...\n")
        test_get_messages(3)
        
        # Uncomment to test sending email
        # test_send_email("test@example.com", "Test", "Hello from API!")
    else:
        print("Gmail is not authenticated. Run 'python setup_gmail.py' to authenticate.\n")
    
    print("=" * 60)
    print("Tests completed!")
    print("=" * 60)

