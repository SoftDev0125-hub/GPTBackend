# Quick Start Guide - Gmail Authentication

## Step 1: Get Authorization URL

Visit this URL in your browser (or use the API):
```
http://localhost:8000/gmail/auth/url
```

Or run:
```powershell
Invoke-WebRequest -Uri http://localhost:8000/gmail/auth/url -UseBasicParsing
```

## Step 2: Authorize Gmail Access

1. Copy the `auth_url` from the response
2. Open it in your browser
3. Sign in with your Google account
4. Click "Allow" to grant permissions
5. Copy the authorization code that appears

## Step 3: Complete Authentication

### Option A: Using the helper script
```bash
python complete_gmail_auth.py YOUR_AUTH_CODE
```

### Option B: Using PowerShell
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/gmail/auth/callback?code=YOUR_AUTH_CODE" -Method POST
```

### Option C: Using curl
```bash
curl -X POST "http://localhost:8000/gmail/auth/callback?code=YOUR_AUTH_CODE"
```

## Step 4: Verify Authentication

Check if authentication was successful:
```powershell
Invoke-WebRequest -Uri http://localhost:8000/gmail/auth/status -UseBasicParsing
```

You should see: `{"authenticated": true, "message": "Authenticated"}`

## Step 5: Test Gmail Endpoints

Now you can test sending emails:
```powershell
$body = @{
    to = "test@example.com"
    subject = "Test"
    body = "Hello from API!"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/gmail/send -Method POST -Body $body -ContentType "application/json"
```

## Troubleshooting

- **"credentials.json not found"**: Make sure you've downloaded OAuth credentials from Google Cloud Console
- **"Invalid code"**: The authorization code expires quickly. Get a new one if it doesn't work
- **"Token expired"**: Delete `token.json` and re-authenticate

