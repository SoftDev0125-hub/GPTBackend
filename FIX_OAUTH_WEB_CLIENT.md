# Fix for Web Application OAuth Client

If you're getting the error: **"Error 400: redirect_uri_mismatch"**, it means your OAuth credentials were created as a **Web application** instead of a **Desktop app**.

## Solution Options

### Option 1: Create a Desktop App OAuth Client (Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Click **"Create Credentials"** > **"OAuth client ID"**
3. Select **"Desktop app"** as the application type
4. Download the credentials JSON file
5. Replace your current `credentials.json` with the new one
6. Try the authentication again

### Option 2: Use Web Application with Localhost Redirect

If you want to keep using a Web application OAuth client:

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Click on your OAuth 2.0 Client ID
3. Under **"Authorized redirect URIs"**, click **"Add URI"**
4. Add: `http://localhost:8000/oauth2callback`
5. Save the changes
6. Get a new authorization URL: `http://localhost:8000/gmail/auth/url`
7. Visit the URL and authorize
8. After authorization, you'll be redirected to `http://localhost:8000/oauth2callback` with the code
9. The authentication will complete automatically

### Option 3: Manual Code Entry (Current Method)

The updated code now supports both Desktop and Web clients. For Web clients using manual code entry:

1. Get authorization URL: `http://localhost:8000/gmail/auth/url`
2. Visit the URL in your browser
3. After authorizing, you'll see an error page (this is normal for web clients with manual entry)
4. **Copy the authorization code from the URL** (it will be in the URL as `?code=...`)
5. Use the code to complete authentication:
   ```bash
   python complete_gmail_auth.py YOUR_CODE
   ```

## How to Get the Code from Error Page

When you visit the authorization URL with a Web client, you might see an error page. The authorization code is in the URL:

```
https://accounts.google.com/o/oauth2/auth?...&code=4/0AeanR...&scope=...
```

Copy the `code` parameter value (everything after `code=` and before the next `&`).

## Quick Test

After fixing, test authentication:
```powershell
Invoke-WebRequest -Uri http://localhost:8000/gmail/auth/status -UseBasicParsing
```

You should see: `{"authenticated": true}`

