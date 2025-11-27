# How to Integrate Your Server with ChatGPT

This guide will help you connect your deployed server to ChatGPT so you can:
- ✅ Say "Send 'hello' to email@example.com" → ChatGPT sends the email
- ✅ Say "Launch Notepad" → ChatGPT starts the app
- ✅ Say "Read my emails" → ChatGPT reads your Gmail

## Prerequisites

- ✅ Your API deployed to Railway (or ngrok)
- ✅ Railway public URL (e.g., `https://your-app.up.railway.app`)
- ✅ Gmail authenticated on your deployed API
- ✅ OpenAI account with API access

## Step 1: Get Your Railway URL

1. Go to https://railway.app
2. Click on your deployed service
3. Copy your **Public URL**
   - Example: `https://chatgptserver-production-xxxx.up.railway.app`
4. **Test it works:**
   - Open: `https://your-url/health`
   - Should show: `{"status":"healthy"}`

## Step 2: Create OpenAI Assistant

1. **Go to OpenAI Platform:**
   - Visit: https://platform.openai.com/assistants
   - Sign in (you need an OpenAI account with API access)

2. **Create New Assistant:**
   - Click **"Create"** or **"+ New Assistant"**
   - **Name:** "Gmail & App Control Assistant"
   - **Model:** Choose `gpt-4-turbo-preview` or `gpt-4o` (recommended)

## Step 3: Add Instructions

In the **"Instructions"** field, paste this:

```
You are a helpful assistant that can:
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

When the user says:
- "Send 'hello' to email@example.com" → Call /gmail/send with to=email@example.com, body="hello"
- "Send a message to email@example.com" → Extract the message and email, call /gmail/send
- "Launch [app name]" or "Start [app name]" → Call /apps/control with app_name=[app name], action="start"
- "Open [app name]" → Same as launch/start
- "Close [app name]" or "Stop [app name]" → Call /apps/control with action="stop"
```

## Step 4: Connect to Your API (Most Important!)

This is the step that actually connects ChatGPT to your server:

1. **Find "Actions" Section:**
   - Scroll down in the assistant settings
   - Look for **"Actions"** or **"Functions"** section

2. **Add Action:**
   - Click **"Add Action"** or **"Add Function"** button
   - Select **"Import from URL"**

3. **Enter Your OpenAPI Schema URL:**
   ```
   https://your-railway-url/openapi.json
   ```
   
   **Replace with your actual Railway URL:**
   - Example: `https://chatgptserver-production-xxxx.up.railway.app/openapi.json`
   - Make sure it's the full URL ending with `/openapi.json`

4. **Verify Import:**
   - OpenAI will fetch your API schema
   - You should see all your endpoints listed
   - If there's an error, check that your URL is accessible

5. **Save the Assistant:**
   - Click **"Save"** button
   - Wait for validation to complete

## Step 5: Test the Integration

1. **Start a Conversation:**
   - Go to your assistant
   - Click **"New Chat"** or start a conversation

2. **Test Sending Email:**
   ```
   Send 'hello' to abelsimbulan1@outlook.com
   ```
   
   **What happens:**
   - ChatGPT calls: `POST /gmail/send`
   - Sends: `{to: "abelsimbulan1@outlook.com", subject: "Message from ChatGPT", body: "hello"}`
   - Your server sends the email via Gmail
   - ChatGPT confirms: "I've sent the email 'hello' to abelsimbulan1@outlook.com"

3. **Test Launching Apps:**
   ```
   Launch Notepad
   ```
   or
   ```
   Start Calculator
   ```
   
   **What happens:**
   - ChatGPT calls: `POST /apps/control`
   - Sends: `{app_name: "notepad", action: "start"}`
   - Your server starts the app
   - ChatGPT confirms: "I've started Notepad"

4. **Test Reading Emails:**
   ```
   Read my latest 5 emails
   ```
   
   **What happens:**
   - ChatGPT calls: `GET /gmail/messages?max_results=5`
   - Your server returns the emails
   - ChatGPT summarizes them for you

## Example Conversations

### Example 1: Send Email
**You:** "Send 'hello' to abelsimbulan1@outlook.com"

**ChatGPT:**
- *[Calls your API: POST /gmail/send]*
- "I've sent the email 'hello' to abelsimbulan1@outlook.com. The message was sent successfully!"

### Example 2: Launch App
**You:** "Launch Notepad"

**ChatGPT:**
- *[Calls your API: POST /apps/control with {app_name: "notepad", action: "start"}]*
- "I've started Notepad for you. The application is now running."

### Example 3: Stop App
**You:** "Close Chrome"

**ChatGPT:**
- *[Calls your API: POST /apps/control with {app_name: "chrome", action: "stop"}]*
- "I've stopped Chrome. The application has been closed."

### Example 4: Read Emails
**You:** "What are my latest emails?"

**ChatGPT:**
- *[Calls your API: GET /gmail/messages?max_results=10]*
- "Here are your latest emails: [summarizes the emails]"

## Troubleshooting

### "Cannot reach API" Error

**Problem:** ChatGPT can't connect to your server

**Solutions:**
1. Verify Railway service is running (check Railway dashboard)
2. Test your URL: `https://your-url/health` (should work in browser)
3. Test OpenAPI schema: `https://your-url/openapi.json` (should show JSON)
4. Make sure URL uses HTTPS (not HTTP)
5. Check Railway logs for errors

### "Actions not working"

**Problem:** ChatGPT doesn't call your API

**Solutions:**
1. Verify Actions section shows your endpoints
2. Check that OpenAPI schema imported successfully
3. Re-import the schema if needed
4. Make sure instructions are clear about when to use endpoints

### "Email not sending"

**Problem:** Email command doesn't work

**Solutions:**
1. Check Gmail authentication: `https://your-url/gmail/auth/status`
2. Should return: `{"authenticated": true}`
3. If not authenticated, upload `token.json` to Railway or re-authenticate

### "App not launching"

**Problem:** App control doesn't work

**Solutions:**
1. Check available apps: `https://your-url/apps/list`
2. Verify app name is correct (case-sensitive)
3. Check Railway logs for errors
4. Note: Apps run on Railway's server, not your local computer (if deployed)

## Important Notes

### ⚠️ App Control Limitation

**If deployed to Railway:**
- Apps will run on Railway's servers, not your local computer
- This means "Launch Notepad" won't open Notepad on your PC
- It will try to run on Railway's Linux server (which may not have Windows apps)

**Solutions:**
1. **For local app control:** Use ngrok instead of Railway
2. **For cloud deployment:** Only Gmail features will work properly
3. **Hybrid approach:** Keep app control local (ngrok) + Gmail on Railway

### 🔒 Security

- Your API is currently public (no authentication)
- Anyone with the URL can call your endpoints
- Consider adding API key authentication for production

## Quick Reference

### Your API Endpoints:

**Gmail:**
- `GET /gmail/messages` - Read emails
- `POST /gmail/send` - Send email
- `POST /gmail/reply` - Reply to email

**App Control:**
- `POST /apps/control` - Start/stop apps
- `GET /apps/list` - List available apps

### Commands ChatGPT Understands:

- "Send 'message' to email@example.com"
- "Send a message to email@example.com"
- "Launch [app name]"
- "Start [app name]"
- "Open [app name]"
- "Close [app name]"
- "Stop [app name]"
- "Read my emails"
- "What are my latest emails?"

---

**You're all set!** Once connected, you can control Gmail and apps through natural language with ChatGPT.

