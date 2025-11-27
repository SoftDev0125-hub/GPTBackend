# ChatGPT Integration - Step by Step Guide

## ✅ What's Ready

- ✅ Server running at `http://localhost:8000`
- ✅ Gmail authenticated
- ✅ OpenAPI schema generated (`openapi_schema.json`)
- ✅ Assistant instructions created (`assistant_instructions.txt`)

## Step 1: Make Your API Publicly Accessible

### Option A: Using ngrok (Recommended for Testing)

1. **Install ngrok:**
   - Download from: https://ngrok.com/download
   - Extract and add to PATH, or use the full path

2. **Start ngrok:**
   ```bash
   ngrok http 8000
   ```

3. **Copy the HTTPS URL:**
   - You'll see something like: `https://abc123.ngrok.io`
   - Copy this URL - you'll need it for Step 2

4. **Keep ngrok running** while using ChatGPT

### Option B: Deploy to Cloud (Production)

Deploy your FastAPI app to:
- **Railway**: https://railway.app (easiest)
- **Heroku**: https://heroku.com
- **DigitalOcean**: https://digitalocean.com
- **AWS/Azure/GCP**: Any cloud provider

## Step 2: Create OpenAI Assistant

1. **Go to OpenAI Platform:**
   - Visit: https://platform.openai.com/assistants
   - Sign in or create an account

2. **Create New Assistant:**
   - Click "Create" or "New Assistant"
   - Name it: "Gmail & App Control Assistant"

3. **Add Instructions:**
   - Copy the content from `assistant_instructions.txt`
   - Paste into the "Instructions" field

4. **Add Actions (Function Calling):**
   - Click "Add Action" or "Add Function"
   - Select "Import from URL" or "Import from File"
   
   **If using ngrok:**
   - Select "Import from URL"
   - Enter: `https://your-ngrok-url.ngrok.io/openapi.json`
   - Replace `your-ngrok-url` with your actual ngrok URL
   
   **OR if using file:**
   - Select "Import from File"
   - Upload: `openapi_schema.json`

5. **Save the Assistant**

## Step 3: Test the Integration

1. **Start a conversation** with your assistant

2. **Try these commands:**
   - "Send 'hi' to abel@example.com"
   - "Read my latest 5 emails"
   - "Start Notepad"
   - "Stop Chrome"
   - "Reply to the email from john@example.com with 'Thanks for your message'"

3. **ChatGPT will automatically:**
   - Call your API endpoints
   - Execute the actions
   - Report back the results

## Example Conversation

**You:** "Send 'hi' to abel@example.com"

**ChatGPT:** *[Calls POST /gmail/send with {to: "abel@example.com", subject: "Message from ChatGPT", body: "hi"}]*

**ChatGPT:** "I've sent the email 'hi' to abel@example.com. The message was sent successfully!"

## Troubleshooting

### "Connection refused" or "Cannot reach API"
- Make sure ngrok is running: `ngrok http 8000`
- Check that your server is running: `python run.py`
- Verify the ngrok URL is correct in OpenAI Assistant settings

### "401 Unauthorized" or "403 Forbidden"
- Your API doesn't have authentication yet (this is fine for local testing)
- For production, add API key authentication (see `chatgpt_integration.md`)

### "CORS error"
- CORS is already configured in `main.py` to allow all origins
- If issues persist, check that your server is accessible

### Actions not working
- Verify the OpenAPI schema URL is accessible
- Check that all endpoints are listed in the schema
- Make sure the assistant has the correct instructions

## Security Notes

⚠️ **For Local Testing (ngrok):**
- ngrok URLs are temporary and change each time you restart
- Only use for testing, not production
- Your API is publicly accessible while ngrok is running

🔒 **For Production:**
- Deploy to a proper cloud service
- Add API key authentication
- Use HTTPS
- Restrict CORS to OpenAI domains only

## Quick Reference

### API Endpoints Available to ChatGPT:

**Gmail:**
- `GET /gmail/messages` - Read emails
- `POST /gmail/send` - Send email
- `POST /gmail/reply` - Reply to email

**App Control:**
- `POST /apps/control` - Start/stop apps
- `GET /apps/list` - List available apps

### Files Created:
- `openapi_schema.json` - OpenAPI schema for ChatGPT
- `assistant_instructions.txt` - Instructions for the assistant
- `setup_chatgpt.py` - Setup helper script

## Next Steps After Setup

1. Test all functionality with ChatGPT
2. Customize assistant instructions for your needs
3. Add more apps to `app_config.json` if needed
4. Consider deploying to production for permanent access
5. Add API key authentication for security

---

**Need Help?** Check `chatgpt_integration.md` for detailed information.

