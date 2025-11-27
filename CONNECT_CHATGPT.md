# How to Connect Your Server with ChatGPT

## Prerequisites Checklist

- ✅ Server running at `http://localhost:8000`
- ✅ Gmail authenticated
- ✅ OpenAPI schema generated (`openapi_schema.json`)
- ✅ Assistant instructions ready (`assistant_instructions.txt`)

## Step-by-Step Connection Guide

### Step 1: Make Your API Publicly Accessible

You need to expose your local server so ChatGPT can access it. Choose one option:

#### Option A: Deploy to Railway (Recommended - Permanent)

1. **Create Railway Account:**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository (or create one if needed)

3. **Configure Environment:**
   - Railway will auto-detect Python
   - Add environment variables if needed:
     - `GOOGLE_CREDENTIALS_PATH=credentials.json`
     - `GOOGLE_TOKEN_PATH=token.json`

4. **Upload Credentials:**
   - In Railway dashboard, go to your service
   - Click "Variables" tab
   - Upload `credentials.json` and `token.json` as files
   - Or paste their contents as environment variables

5. **Deploy:**
   - Railway will automatically deploy
   - Get your public URL: `https://your-app-name.up.railway.app`

6. **Test Your Deployed API:**
   ```
   https://your-app-name.up.railway.app/health
   ```

#### Option B: Use ngrok (Quick Testing - Temporary)

1. **Install ngrok:**
   - Download: https://ngrok.com/download
   - Extract and run: `ngrok http 8000`

2. **Get Your URL:**
   - Copy the HTTPS URL: `https://abc123.ngrok.io`
   - Keep ngrok running

3. **Note:** URL changes each time you restart ngrok

### Step 2: Create OpenAI Assistant

1. **Go to OpenAI Platform:**
   - Visit: https://platform.openai.com/assistants
   - Sign in or create account

2. **Create New Assistant:**
   - Click "Create" or "+ New Assistant"
   - Name: "Gmail & App Control Assistant"

3. **Add Instructions:**
   - Open `assistant_instructions.txt`
   - Copy all the content
   - Paste into the "Instructions" field in OpenAI

4. **Select Model:**
   - Choose: `gpt-4-turbo-preview` or `gpt-4o`
   - (gpt-3.5-turbo also works but less capable)

### Step 3: Add Actions (Connect to Your API)

1. **In the Assistant Settings:**
   - Scroll to "Actions" or "Functions" section
   - Click "Add Action" or "Add Function"

2. **Import OpenAPI Schema:**
   
   **If using Railway:**
   - Select "Import from URL"
   - Enter: `https://your-app-name.up.railway.app/openapi.json`
   - Replace with your actual Railway URL
   
   **If using ngrok:**
   - Select "Import from URL"
   - Enter: `https://your-ngrok-url.ngrok.io/openapi.json`
   - Replace with your actual ngrok URL
   
   **OR upload file:**
   - Select "Import from File"
   - Upload: `openapi_schema.json`

3. **Save the Assistant**

### Step 4: Test the Connection

1. **Start a Conversation:**
   - Go to your assistant
   - Click "New Chat" or start a conversation

2. **Test Commands:**
   ```
   Send 'hi' to abelsimbulan1@outlook.com
   ```
   
   Or:
   ```
   Read my latest 5 emails
   ```
   
   Or:
   ```
   Start Notepad
   ```

3. **What Should Happen:**
   - ChatGPT understands your command
   - Calls your API endpoint
   - Executes the action
   - Reports back the result

## Troubleshooting

### "Connection refused" or "Cannot reach API"
- **Railway:** Check deployment logs, ensure service is running
- **ngrok:** Make sure ngrok is running: `ngrok http 8000`
- **Both:** Verify the URL is correct in Assistant settings

### "401 Unauthorized" or "403 Forbidden"
- Your API doesn't require authentication (this is fine for now)
- If you added API key auth, make sure it's configured in Assistant

### Actions not appearing
- Verify OpenAPI schema URL is accessible
- Check that schema loads: `https://your-url/openapi.json`
- Make sure you saved the Assistant after adding Actions

### Email not sending
- Check Gmail authentication: `https://your-url/gmail/auth/status`
- Verify `token.json` is uploaded to Railway (if deployed)
- Re-authenticate if needed

## Quick Verification

Test your public API is accessible:

**Health Check:**
```bash
curl https://your-url/health
```

**OpenAPI Schema:**
```bash
curl https://your-url/openapi.json
```

Both should return JSON responses.

## Example Conversation Flow

**You:** "Send 'hi' to abelsimbulan1@outlook.com"

**ChatGPT:** 
- *[Calls POST /gmail/send]*
- "I've sent the email 'hi' to abelsimbulan1@outlook.com. The message was sent successfully!"

**You:** "Read my latest emails"

**ChatGPT:**
- *[Calls GET /gmail/messages?max_results=10]*
- Shows you a summary of your latest emails

## Next Steps After Connection

1. ✅ Test all functionality
2. ✅ Customize assistant instructions if needed
3. ✅ Add more apps to control (edit `app_config.json`)
4. ✅ Consider adding API key authentication for security
5. ✅ Monitor usage and logs

---

**Need Help?** 
- Check deployment: `DEPLOY_RAILWAY.md`
- Full setup guide: `CHATGPT_SETUP.md`
- Integration details: `chatgpt_integration.md`

