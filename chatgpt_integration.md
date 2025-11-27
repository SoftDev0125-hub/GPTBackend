# ChatGPT Integration Guide

This guide explains how to connect your GPT Backend API to ChatGPT using OpenAI's Assistant API with Actions (Function Calling).

## Prerequisites

1. Your backend server running at `http://localhost:8000` (or deployed URL)
2. OpenAI API key
3. For local testing: ngrok or similar tunneling service

## Step 1: Make Your API Publicly Accessible

### Option A: Using ngrok (for local testing)

1. Install ngrok: https://ngrok.com/download
2. Start your backend server: `python run.py`
3. In another terminal, run: `ngrok http 8000`
4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### Option B: Deploy to a Server

Deploy your FastAPI app to:
- Heroku
- Railway
- DigitalOcean
- AWS
- Any cloud provider that supports Python

## Step 2: Get Your OpenAPI Schema

Your FastAPI app automatically generates an OpenAPI schema. Access it at:

```
http://localhost:8000/openapi.json
```

Or if using ngrok:
```
https://your-ngrok-url.ngrok.io/openapi.json
```

Save this JSON file or note the URL.

## Step 3: Create OpenAI Assistant with Actions

### Using OpenAI API (Python)

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Create assistant with actions
assistant = client.beta.assistants.create(
    name="Gmail & App Control Assistant",
    instructions="""You are a helpful assistant that can:
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
    
    Always be helpful and confirm actions before executing them.""",
    model="gpt-4-turbo-preview",
    tools=[{
        "type": "function",
        "function": {
            "name": "call_api",
            "description": "Call the GPT Backend API",
            "parameters": {
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST"],
                        "description": "HTTP method"
                    },
                    "endpoint": {
                        "type": "string",
                        "description": "API endpoint path (e.g., /gmail/send, /apps/control)"
                    },
                    "body": {
                        "type": "object",
                        "description": "Request body for POST requests"
                    }
                },
                "required": ["method", "endpoint"]
            }
        }
    }]
)
```

### Using OpenAI Actions (Recommended)

OpenAI Actions allows you to directly connect your OpenAPI schema:

1. Go to https://platform.openai.com/
2. Navigate to "Assistants" > "Create Assistant"
3. In the "Actions" section, click "Add Action"
4. Select "Import from URL" or "Import from File"
5. Provide your OpenAPI schema URL or upload the JSON file
6. Configure the assistant with instructions

## Step 4: Example Usage

### Example 1: "Send 'hi' to abel@example.com"

ChatGPT will call:
```json
POST /gmail/send
{
  "to": "abel@example.com",
  "subject": "Message from ChatGPT",
  "body": "hi"
}
```

### Example 2: "Read my latest emails"

ChatGPT will call:
```
GET /gmail/messages?max_results=10
```

### Example 3: "Start Notepad"

ChatGPT will call:
```json
POST /apps/control
{
  "app_name": "notepad",
  "action": "start"
}
```

## Step 5: Testing the Integration

1. Create a thread with the assistant
2. Send a message like: "Send 'Hello' to test@example.com"
3. The assistant should call your API and execute the action
4. Check the response and confirm the action was successful

## API Endpoints Summary

### Gmail Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/gmail/messages` | GET | Get Gmail messages |
| `/gmail/messages/{id}` | GET | Get specific message |
| `/gmail/send` | POST | Send new email |
| `/gmail/reply` | POST | Reply to email |
| `/gmail/auth/status` | GET | Check auth status |
| `/gmail/auth/url` | GET | Get OAuth URL |

### App Control Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/apps/control` | POST | Start/stop app |
| `/apps/list` | GET | List available apps |

## Security Considerations

1. **API Authentication**: Add API key authentication to your endpoints
2. **HTTPS**: Always use HTTPS in production
3. **CORS**: Restrict CORS origins to OpenAI domains
4. **Rate Limiting**: Implement rate limiting
5. **Input Validation**: Already handled by Pydantic models

## Adding API Key Authentication

To secure your API, add authentication:

```python
from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY", "your-secret-key")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.post("/gmail/send")
async def send_email(request: SendEmailRequest, api_key: str = Depends(verify_api_key)):
    # ... existing code
```

Then configure OpenAI to send the API key in headers:
```
X-API-Key: your-secret-key
```

## Troubleshooting

1. **Connection refused**: Make sure your server is running
2. **CORS errors**: Check CORS settings in main.py
3. **Authentication errors**: Verify Gmail OAuth setup
4. **App not found**: Check app_config.json for correct app names

## Next Steps

1. Test all endpoints using the interactive docs at `/docs`
2. Set up Gmail authentication: `python setup_gmail.py`
3. Deploy your API to a public server
4. Create your OpenAI Assistant with Actions
5. Test the integration with various commands

