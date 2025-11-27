"""
Gmail Service - Handles Gmail API operations
"""
import os
import base64
import json
from typing import List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import asyncio
from functools import lru_cache

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.modify']


class GmailService:
    def __init__(self):
        self.credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
        self.token_path = os.getenv('GOOGLE_TOKEN_PATH', 'token.json')
        self.service = None
        self._credentials = None

    async def _get_service(self):
        """Get or create Gmail API service"""
        if self.service is None:
            await self._authenticate()
        return self.service

    async def _authenticate(self):
        """Authenticate and create Gmail API service"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            except Exception as e:
                print(f"Error loading credentials: {e}")
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    creds = None
            
            if not creds:
                raise Exception(
                    "Gmail not authenticated. Please use /gmail/auth/url to get authorization URL, "
                    "then use /gmail/auth/callback with the authorization code."
                )
            
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        self._credentials = creds
        self.service = build('gmail', 'v1', credentials=creds)

    async def is_authenticated(self) -> bool:
        """Check if Gmail is authenticated"""
        try:
            if os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
                if creds and creds.valid:
                    return True
                elif creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                        with open(self.token_path, 'w') as token:
                            token.write(creds.to_json())
                        return True
                    except:
                        return False
            return False
        except:
            return False

    def _detect_client_type(self) -> str:
        """Detect OAuth client type from credentials file"""
        try:
            with open(self.credentials_path, 'r') as f:
                creds_data = json.load(f)
                # Check if it's a web client (has redirect_uris) or installed app
                if 'installed' in creds_data:
                    return 'installed'
                elif 'web' in creds_data:
                    return 'web'
                else:
                    # Default to installed for backward compatibility
                    return 'installed'
        except Exception:
            return 'installed'  # Default
    
    async def get_authorization_url(self) -> str:
        """Get OAuth authorization URL"""
        if not os.path.exists(self.credentials_path):
            raise Exception(
                f"Credentials file not found at {self.credentials_path}. "
                "Please download OAuth 2.0 credentials from Google Cloud Console."
            )
        
        client_type = self._detect_client_type()
        
        if client_type == 'installed':
            # Desktop/Installed app flow
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, SCOPES)
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'  # For installed apps
        else:
            # Web application flow - use localhost redirect
            flow = Flow.from_client_secrets_file(
                self.credentials_path, SCOPES)
            # Use localhost redirect URI for web apps
            # Make sure this is added to your OAuth client's authorized redirect URIs
            flow.redirect_uri = 'http://localhost:8000/oauth2callback'
        
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        return auth_url

    async def handle_oauth_callback(self, code: str, redirect_uri: Optional[str] = None):
        """Handle OAuth callback and store credentials"""
        if not os.path.exists(self.credentials_path):
            raise Exception(f"Credentials file not found at {self.credentials_path}")
        
        client_type = self._detect_client_type()
        
        if client_type == 'installed':
            # Desktop/Installed app flow
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, SCOPES)
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        else:
            # Web application flow
            flow = Flow.from_client_secrets_file(
                self.credentials_path, SCOPES)
            # Use provided redirect_uri or default to localhost
            flow.redirect_uri = redirect_uri or 'http://localhost:8000/oauth2callback'
        
        # Fetch token
        flow.fetch_token(code=code)
        creds = flow.credentials
        
        # Save credentials
        with open(self.token_path, 'w') as token:
            token.write(creds.to_json())
        
        self._credentials = creds
        self.service = build('gmail', 'v1', credentials=creds)

    async def get_messages(self, max_results: int = 10, query: Optional[str] = None) -> List[dict]:
        """Get Gmail messages"""
        service = await self._get_service()
        
        try:
            # Build query
            query_str = query if query else ''
            
            # Get message list
            results = service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q=query_str
            ).execute()
            
            messages = results.get('messages', [])
            
            # Get full message details
            message_list = []
            for msg in messages:
                message = await self._get_message_details(service, msg['id'])
                if message:
                    message_list.append(message)
            
            return message_list
        except HttpError as error:
            raise Exception(f"An error occurred: {error}")

    async def _get_message_details(self, service, message_id: str) -> Optional[dict]:
        """Get detailed message information"""
        try:
            message = service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = message['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            to_emails = [h['value'] for h in headers if h['name'] == 'To']
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extract body
            body = self._extract_body(message['payload'])
            
            return {
                'id': message['id'],
                'thread_id': message['threadId'],
                'from_email': from_email,
                'to': to_emails,
                'subject': subject,
                'body': body,
                'date': date,
                'snippet': message.get('snippet', '')
            }
        except Exception as e:
            print(f"Error getting message details: {e}")
            return None

    def _extract_body(self, payload: dict) -> str:
        """Extract email body from payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    data = part['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body

    async def get_message(self, message_id: str) -> dict:
        """Get a specific message by ID"""
        service = await self._get_service()
        message = await self._get_message_details(service, message_id)
        if not message:
            raise Exception(f"Message {message_id} not found")
        return message

    async def send_email(self, to: str, subject: str, body: str,
                        cc: Optional[List[str]] = None,
                        bcc: Optional[List[str]] = None) -> str:
        """Send an email"""
        service = await self._get_service()
        
        try:
            # Create message
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = ', '.join(cc)
            if bcc:
                message['bcc'] = ', '.join(bcc)
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('utf-8')
            
            # Send message
            send_message = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return send_message['id']
        except HttpError as error:
            raise Exception(f"An error occurred: {error}")

    async def reply_to_email(self, thread_id: str, body: str,
                            in_reply_to: Optional[str] = None) -> str:
        """Reply to an email thread"""
        service = await self._get_service()
        
        try:
            # Get original message to extract headers
            original_message = service.users().messages().get(
                userId='me',
                id=thread_id,
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Message-ID']
            ).execute()
            
            headers = original_message['payload'].get('headers', [])
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), '')
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            message_id = next((h['value'] for h in headers if h['name'] == 'Message-ID'), '')
            
            # Create reply message
            message = MIMEText(body)
            message['to'] = from_email
            message['subject'] = f"Re: {subject}" if not subject.startswith('Re:') else subject
            if message_id:
                message['In-Reply-To'] = message_id
                message['References'] = message_id
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('utf-8')
            
            # Send reply
            send_message = service.users().messages().send(
                userId='me',
                body={
                    'raw': raw_message,
                    'threadId': thread_id
                }
            ).execute()
            
            return send_message['id']
        except HttpError as error:
            raise Exception(f"An error occurred: {error}")

