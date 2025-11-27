# GPT Backend - Gmail & App Control API

A Python FastAPI backend that enables ChatGPT to manage your Gmail account and control applications on your computer.

## Features

- 📧 **Gmail Management**
  - Read Gmail messages
  - Send new emails
  - Reply to emails
  - Full Gmail API integration with OAuth 2.0

- 🖥️ **App Control**
  - Start applications
  - Stop applications
  - List available apps
  - Customizable app configurations

- 🤖 **ChatGPT Integration**
  - RESTful API endpoints
  - Compatible with OpenAI Function Calling / Actions
  - CORS enabled for cross-origin requests

## Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Gmail API enabled
- OAuth 2.0 credentials from Google Cloud Console

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Download the credentials JSON file
   - Save it as `credentials.json` in the project root

### 3. Environment Configuration

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` if needed (defaults should work for most cases).

### 4. Run the Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

## Gmail Authentication

### First Time Setup

1. Start the server
2. Visit: `http://localhost:8000/gmail/auth/url`
3. Copy the `auth_url` from the response
4. Open the URL in your browser
5. Authorize the application
6. Copy the authorization code
7. Send a POST request to `http://localhost:8000/gmail/auth/callback?code=YOUR_CODE`

Or use curl:

```bash
# Get auth URL
curl http://localhost:8000/gmail/auth/url

# After authorizing, use the code:
curl -X POST "http://localhost:8000/gmail/auth/callback?code=YOUR_AUTH_CODE"
```

After authentication, a `token.json` file will be created and used for subsequent requests.

## API Endpoints

### Gmail Endpoints

- `GET /gmail/messages` - Get Gmail messages (supports `max_results` and `query` parameters)
- `GET /gmail/messages/{message_id}` - Get a specific message
- `POST /gmail/send` - Send a new email
- `POST /gmail/reply` - Reply to an email
- `GET /gmail/auth/status` - Check authentication status
- `GET /gmail/auth/url` - Get OAuth authorization URL
- `POST /gmail/auth/callback` - Handle OAuth callback

### App Control Endpoints

- `POST /apps/control` - Start or stop an application
- `GET /apps/list` - List available apps

## Usage Examples

### Send an Email

```bash
curl -X POST "http://localhost:8000/gmail/send" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "abel@example.com",
    "subject": "Hello",
    "body": "Hi"
  }'
```

### Read Messages

```bash
curl "http://localhost:8000/gmail/messages?max_results=5"
```

### Start an App

```bash
curl -X POST "http://localhost:8000/apps/control" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "notepad",
    "action": "start"
  }'
```

### Stop an App

```bash
curl -X POST "http://localhost:8000/apps/control" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "notepad",
    "action": "stop"
  }'
```

## Configuring Apps

Default apps are configured in `services/app_control_service.py`. You can add custom apps by:

1. Editing `app_config.json` (created automatically on first run)
2. Or programmatically using the service methods

Example `app_config.json`:

```json
{
  "myapp": {
    "path": "C:\\Path\\To\\MyApp.exe",
    "type": "executable"
  },
  "customcommand": {
    "path": "mycommand",
    "type": "command"
  }
}
```

## ChatGPT Integration

To use this with ChatGPT/OpenAI:

1. **Using OpenAI Actions (Recommended)**
   - Deploy this API to a publicly accessible server (or use ngrok for local testing)
   - Create an OpenAI Assistant with Actions
   - Provide the OpenAPI schema (available at `http://localhost:8000/openapi.json`)
   - Configure the assistant to use your API endpoints

2. **Using Function Calling**
   - Use the API endpoints as functions in your ChatGPT integration
   - Map user requests to appropriate API calls

### Example: "Send 'hi' to abel"

When ChatGPT receives this request, it should call:

```json
POST /gmail/send
{
  "to": "abel@example.com",
  "subject": "Message from ChatGPT",
  "body": "hi"
}
```

## Local Development with ngrok (for ChatGPT testing)

If you want to test with ChatGPT locally:

1. Install ngrok: https://ngrok.com/
2. Start your server: `python main.py`
3. In another terminal: `ngrok http 8000`
4. Use the ngrok URL (e.g., `https://abc123.ngrok.io`) as your API base URL in ChatGPT configuration

## Security Considerations

- **Never commit `credentials.json` or `token.json`** to version control
- Use environment variables for sensitive configuration
- In production, restrict CORS origins to specific domains
- Consider adding authentication/authorization to the API
- Use HTTPS in production

## Troubleshooting

### Gmail Authentication Issues

- Ensure `credentials.json` is in the project root
- Check that Gmail API is enabled in Google Cloud Console
- Verify OAuth consent screen is configured
- Delete `token.json` and re-authenticate if needed

### App Control Issues

- Ensure app paths are correct
- On Windows, use full paths for executables
- Some apps may require administrator privileges
- Check that the app name matches the configuration

## License

MIT License - feel free to use and modify as needed.

