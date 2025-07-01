import os
import base64
from base64 import urlsafe_b64decode
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from typing import Any
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv(override=True)

# Set OpenAI and Google credentials as environment variables (for libraries)
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is not None:
    os.environ["OPENAI_API_KEY"] = openai_api_key

google_credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
if google_credentials_path is not None:
    os.environ["GOOGLE_CREDENTIALS_PATH"] = google_credentials_path

# Google API scopes for Calendar and Gmail
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

# Initialize OpenAI LLM with GPT-4 model 
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Function to get Google API credentials and handle OAuth flow 
def get_google_credentials() -> Credentials:
    """
    Loads Google API credentials from token.json (OAuth) or starts OAuth flow if not available.
    Returns:
        Credentials: Authenticated credentials object.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.environ["GOOGLE_CREDENTIALS_PATH"], SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds # type: ignore


@tool
def authenticate_google(_: str = "") -> str:
    """
    Authenticates Google account and stores token for later use.
    Returns a success or error message.
    """
    try:
        get_google_credentials()
        return "✅ Google authentication successful."
    except Exception as e:
        return f"❌ Google authentication failed: {str(e)}"

@tool
def send_email_tool(email_data: str) -> str:
    """
    Sends an email using Gmail.
    Input example:
    'To: user@example.com | Subject: Demo | Body: This is a test message'
    """
    try:
        parts = dict(p.strip().split(":", 1) for p in email_data.split("|"))
        to = parts["To"].strip()
        subject = parts["Subject"].strip()
        body = parts["Body"].strip()

        creds = get_google_credentials()
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_message = service.users().messages().send(userId="me", body={'raw': raw}).execute()
        return f"✅ Email sent successfully. ID: {send_message['id']}"
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"

@tool
def create_event_tool(event_details: str) -> str:
    """
    Creates a Google Calendar event with Meet link.
    Input format:
    'Title: Demo Meeting | Date: 2025-07-02 | Time: 10:00 | Duration: 1 | Description: Discuss ticket PC-123'
    Returns event and Google Meet links.
    """
    try:
        parts = dict(p.strip().split(":", 1) for p in event_details.split("|"))
        title = parts["Title"].strip()
        date = parts["Date"].strip()
        time_str = parts["Time"].strip()
        duration_hours = float(parts.get("Duration", 1))
        description = parts.get("Description", "").strip()

        start_dt = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + timedelta(hours=duration_hours)

        creds = get_google_credentials()
        service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': title,
            'description': description,
            'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'America/Bogota'},
            'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'America/Bogota'},
            'conferenceData': {
                'createRequest': {
                    'requestId': f"meet-{int(datetime.now().timestamp())}"
                }
            }
        }

        created_event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()

        html_link = created_event.get('htmlLink')
        meet_link = created_event.get('hangoutLink')

        response = f"📅 Event created successfully.\n🔗 Event link: {html_link}"
        if meet_link:
            response += f"\n📹 Google Meet: {meet_link}"
        return response

    except Exception as e:
        return f"❌ Error creating event: {str(e)}"

@tool
def read_email_query(query: str = "subject:[BUG]", max_results: int = 10) -> str:
    """
    Reads emails from Gmail using a specific search query (default: '[BUG]').
    Returns the most recent emails matching the query, showing sender, subject, and plain text body.
    """
    try:
        creds = get_google_credentials()  
        service = build('gmail', 'v1', credentials=creds)
        
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        messages = results.get('messages', [])

        if not messages:
            return "📭 No emails found with the given criteria."

        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            headers = msg_data.get("payload", {}).get("headers", [])
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No subject)")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown)")

            # Extract plain text body
            parts = msg_data.get("payload", {}).get("parts", [])
            body = ""
            for part in parts:
                if part.get("mimeType") == "text/plain":
                    body_data = part.get("body", {}).get("data")
                    if body_data:
                        body = urlsafe_b64decode(body_data.encode("ASCII")).decode("utf-8")
                        break
            # Clean the body text 
            body = re.sub(r"\s+", " ", body).strip()
            emails.append(f"🧾 From: {sender}\n📌 Subject: {subject}\n📄 Body: {body[:500]}...")

        return "\n\n".join(emails)

    except Exception as e:
        return f"❌ Error reading emails: {str(e)}"

@tool
def generate_gmail_query(user_description: str) -> str:
    """
    Converts a natural language description into a Gmail query using fields like subject and from.
    Never use label:. Only use 'subject:' or 'from:' fields and valid Gmail operators.
    Returns only the Gmail query string.
    """
    prompt = f"""
You are a Gmail query generator. Based on the user description, return a valid Gmail query using only:
- subject:[BUG], subject:[FAILURE], etc.
- from:user@example.com
Use OR/AND operators as needed.

Do NOT include label: under any circumstances, even if the user requests it.
Only return the query, without any explanation.

Examples:
"Emails with bugs or failures" → subject:[BUG] OR subject:[FAILURE]
"Emails from production team with bugs" → from:production@company.com AND (subject:[BUG] OR subject:[FAILURE])

Now generate the query for:
\"{user_description}\"
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()  # type: ignore