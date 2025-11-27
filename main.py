"""
GPT Backend - API server for Gmail management and app control
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
from dotenv import load_dotenv

from services.gmail_service import GmailService
from services.app_control_service import AppControlService

load_dotenv()

app = FastAPI(
    title="GPT Backend API",
    description="Backend API for Gmail management and app control",
    version="1.0.0"
)

# CORS middleware to allow ChatGPT/OpenAI to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
gmail_service = GmailService()
app_control_service = AppControlService()


# Pydantic models for request/response
class SendEmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None


class ReplyEmailRequest(BaseModel):
    thread_id: str
    body: str
    in_reply_to: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    thread_id: str
    from_email: str
    to: List[str]
    subject: str
    body: str
    date: str
    snippet: Optional[str] = None


class AppControlRequest(BaseModel):
    app_name: str
    action: str  # "start" or "stop"


class AppControlResponse(BaseModel):
    success: bool
    message: str
    app_name: str
    action: str


# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "GPT Backend API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Gmail endpoints
@app.get("/gmail/messages", response_model=List[MessageResponse])
async def get_messages(max_results: int = 10, query: Optional[str] = None):
    """Get Gmail messages"""
    try:
        messages = await gmail_service.get_messages(max_results=max_results, query=query)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")


@app.get("/gmail/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: str):
    """Get a specific Gmail message by ID"""
    try:
        message = await gmail_service.get_message(message_id)
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching message: {str(e)}")


@app.post("/gmail/send")
async def send_email(request: SendEmailRequest):
    """Send a new email"""
    try:
        message_id = await gmail_service.send_email(
            to=request.to,
            subject=request.subject,
            body=request.body,
            cc=request.cc,
            bcc=request.bcc
        )
        return {
            "success": True,
            "message": "Email sent successfully",
            "message_id": message_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")


@app.post("/gmail/reply")
async def reply_email(request: ReplyEmailRequest):
    """Reply to an email"""
    try:
        message_id = await gmail_service.reply_to_email(
            thread_id=request.thread_id,
            body=request.body,
            in_reply_to=request.in_reply_to
        )
        return {
            "success": True,
            "message": "Reply sent successfully",
            "message_id": message_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error replying to email: {str(e)}")


@app.get("/gmail/auth/status")
async def auth_status():
    """Check Gmail authentication status"""
    try:
        is_authenticated = await gmail_service.is_authenticated()
        return {
            "authenticated": is_authenticated,
            "message": "Authenticated" if is_authenticated else "Not authenticated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking auth status: {str(e)}")


@app.get("/gmail/auth/url")
async def get_auth_url():
    """Get Gmail OAuth authorization URL"""
    try:
        auth_url = await gmail_service.get_authorization_url()
        return {
            "auth_url": auth_url,
            "message": "Visit this URL to authorize Gmail access"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating auth URL: {str(e)}")


@app.post("/gmail/auth/callback")
async def auth_callback(code: str, redirect_uri: Optional[str] = None):
    """Handle OAuth callback and store credentials"""
    try:
        await gmail_service.handle_oauth_callback(code, redirect_uri)
        return {
            "success": True,
            "message": "Gmail authentication successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error handling auth callback: {str(e)}")


@app.get("/oauth2callback")
async def oauth2_callback(code: Optional[str] = None, error: Optional[str] = None):
    """OAuth2 callback endpoint for web applications"""
    if error:
        return {
            "success": False,
            "error": error,
            "message": "OAuth authorization was denied or failed",
            "help": "Please try the authorization process again."
        }
    
    if not code:
        # Return HTML page with instructions when accessed directly
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gmail OAuth Callback</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
                .info { background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .error { background: #ffebee; padding: 15px; border-radius: 5px; margin: 20px 0; }
                code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>Gmail OAuth Callback</h1>
            <div class="error">
                <strong>No authorization code provided</strong>
                <p>This endpoint is called automatically by Google after you authorize the application.</p>
            </div>
            <div class="info">
                <h3>To complete Gmail authentication:</h3>
                <ol>
                    <li>Get the authorization URL: <code>http://localhost:8000/gmail/auth/url</code></li>
                    <li>Visit the URL in your browser</li>
                    <li>Sign in and authorize the application</li>
                    <li>You'll be redirected here automatically with the authorization code</li>
                </ol>
                <p><strong>Note:</strong> Make sure you've added <code>http://localhost:8000/oauth2callback</code> 
                to your OAuth client's authorized redirect URIs in Google Cloud Console.</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    try:
        await gmail_service.handle_oauth_callback(code, redirect_uri='http://localhost:8000/oauth2callback')
        html_success = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gmail Authentication Successful</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; text-align: center; }
                .success { background: #e8f5e9; padding: 20px; border-radius: 5px; margin: 20px 0; }
                .check { color: #4caf50; font-size: 48px; }
            </style>
        </head>
        <body>
            <div class="success">
                <div class="check">✓</div>
                <h2>Gmail Authentication Successful!</h2>
                <p>You can now close this window.</p>
                <p>Your Gmail API access has been configured.</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_success)
    except Exception as e:
        html_error = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
                .error {{ background: #ffebee; padding: 20px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>Authentication Failed</h2>
                <p><strong>Error:</strong> {str(e)}</p>
                <p>Please try the authorization process again.</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_error, status_code=500)


# App control endpoints
@app.post("/apps/control", response_model=AppControlResponse)
async def control_app(request: AppControlRequest):
    """Start or stop an application"""
    try:
        if request.action.lower() == "start":
            result = await app_control_service.start_app(request.app_name)
        elif request.action.lower() == "stop":
            result = await app_control_service.stop_app(request.app_name)
        else:
            raise HTTPException(status_code=400, detail="Action must be 'start' or 'stop'")
        
        return AppControlResponse(
            success=result["success"],
            message=result["message"],
            app_name=request.app_name,
            action=request.action.lower()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error controlling app: {str(e)}")


@app.get("/apps/list")
async def list_apps():
    """List available apps that can be controlled"""
    try:
        apps = await app_control_service.list_available_apps()
        return {
            "apps": apps,
            "message": "Available apps for control"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing apps: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

