#!/usr/bin/env python3
"""
Serverless Outlook-OpenAI Integration for Vercel
Handles email processing with 4-day reply tracking
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler
import requests
import msal
from openai import OpenAI
from dateutil import parser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Email:
    id: str
    subject: str
    sender: str
    body: str
    received_date: datetime
    is_read: bool
    has_replies: bool = False
    last_reply_date: Optional[datetime] = None

class MicrosoftGraphAPI:
    """Handles Microsoft Graph API authentication and operations."""
    
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.tenant_id = os.getenv('TENANT_ID')
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        self.access_token = None
        self.token_expires = None
        
    def authenticate(self):
        """Authenticate with Microsoft Graph API using client credentials flow."""
        try:
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=self.authority,
                client_credential=self.client_secret
            )
            
            result = app.acquire_token_for_client(scopes=self.scope)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                self.token_expires = datetime.now() + timedelta(seconds=result.get("expires_in", 3600))
                logger.info("Successfully authenticated with Microsoft Graph API")
                return True
            else:
                logger.error(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
    
    def _get_headers(self):
        """Get headers for API requests."""
        if not self.access_token or (self.token_expires and datetime.now() >= self.token_expires):
            if not self.authenticate():
                raise Exception("Failed to authenticate with Microsoft Graph API")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def get_emails_needing_replies(self, days_threshold: int = 4) -> List[Email]:
        """Get emails up to 4 days old that haven't been replied to."""
        try:
            # Get emails from the last 7 days (to cover the 4-day threshold)
            cutoff_date = datetime.now() - timedelta(days=7)
            cutoff_str = cutoff_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Query for emails received in the last 7 days
            url = f"https://graph.microsoft.com/v1.0/me/messages"
            params = {
                "$filter": f"receivedDateTime ge {cutoff_str}",
                "$select": "id,subject,from,body,receivedDateTime,isRead",
                "$orderby": "receivedDateTime desc",
                "$top": 100
            }
            
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            
            emails = []
            threshold_date = datetime.now() - timedelta(days=days_threshold)
            
            for item in response.json().get("value", []):
                email = Email(
                    id=item["id"],
                    subject=item.get("subject", "No Subject"),
                    sender=item["from"]["emailAddress"]["address"],
                    body=item["body"]["content"],
                    received_date=parser.parse(item["receivedDateTime"]),
                    is_read=item["isRead"]
                )
                
                # Only process emails up to 4 days old
                if email.received_date >= threshold_date:
                    # Check if this email already has a draft response
                    has_draft = self._check_for_draft_response(email.id)
                    
                    if not has_draft:
                        # Check if you've already replied to this email
                        has_replies = self._check_for_replies(email.id, email.received_date)
                        email.has_replies = has_replies
                        
                        if not has_replies:
                            emails.append(email)
            
            logger.info(f"Found {len(emails)} emails up to {days_threshold} days old needing draft responses")
            return emails
            
        except Exception as e:
            logger.error(f"Error retrieving emails: {str(e)}")
            return []
    
    def _check_for_replies(self, email_id: str, original_date: datetime) -> bool:
        """Check if there are replies to this email after the original date."""
        try:
            # Look for emails with the same subject (Re: pattern) after the original date
            subject_filter = f"subject eq 'Re: {email_id}' or subject eq 'RE: {email_id}'"
            date_filter = f"receivedDateTime gt {original_date.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            
            url = f"https://graph.microsoft.com/v1.0/me/messages"
            params = {
                "$filter": f"({subject_filter}) and ({date_filter})",
                "$select": "id,receivedDateTime",
                "$top": 5
            }
            
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            
            replies = response.json().get("value", [])
            return len(replies) > 0
            
        except Exception as e:
            logger.error(f"Error checking for replies: {str(e)}")
            return False
    
    def _check_for_draft_response(self, email_id: str) -> bool:
        """Check if there's already a draft response for this email."""
        try:
            # Look for drafts with the same subject pattern
            url = f"https://graph.microsoft.com/v1.0/me/mailFolders/Drafts/messages"
            params = {
                "$select": "id,subject",
                "$top": 50
            }
            
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            
            drafts = response.json().get("value", [])
            
            # Check if any draft has a subject that matches this email
            for draft in drafts:
                subject = draft.get("subject", "")
                if email_id in subject or f"Re: {email_id}" in subject:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking for draft responses: {str(e)}")
            return False
    
    def create_draft(self, subject: str, body: str, to_recipients: List[str], reply_to_id: Optional[str] = None) -> bool:
        """Create a draft email."""
        try:
            draft_data = {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": body
                },
                "toRecipients": [
                    {"emailAddress": {"address": email}} for email in to_recipients
                ]
            }
            
            if reply_to_id:
                draft_data["replyTo"] = [{"id": reply_to_id}]
            
            url = "https://graph.microsoft.com/v1.0/me/messages"
            response = requests.post(url, headers=self._get_headers(), json=draft_data)
            response.raise_for_status()
            
            logger.info(f"Created draft email: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating draft: {str(e)}")
            return False

class OpenAIHandler:
    """Handles OpenAI API interactions for email processing."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.allowed_domains = os.getenv('ALLOWED_DOMAINS', '').split(',') if os.getenv('ALLOWED_DOMAINS') else []
    
    def should_process_email(self, email: Email) -> bool:
        """Determine if an email should be processed based on domain filters."""
        if not self.allowed_domains:
            return True
        
        sender_domain = email.sender.split('@')[-1]
        return sender_domain in self.allowed_domains
    
    def generate_draft_response(self, email: Email) -> Optional[str]:
        """Generate a draft response using OpenAI with training system."""
        try:
            days_old = (datetime.now() - email.received_date).days
            
            # Try to use training system if available
            try:
                from training_system import TrainingSystem
                training_system = TrainingSystem()
                
                # Analyze email type
                email_type = training_system.analyze_email_type(email.body)
                
                # Generate customized response
                draft_response = training_system.generate_customized_response(
                    email.body,
                    email_type,
                    "professional",  # Default tone
                    days_old
                )
                
                if draft_response:
                    logger.info(f"Generated customized response for {days_old}-day-old {email_type} email: {email.subject}")
                    return draft_response
                    
            except ImportError:
                logger.info("Training system not available, using default response generation")
            except Exception as e:
                logger.warning(f"Training system failed, falling back to default: {e}")
            
            # Fallback to default response generation
            if days_old == 0:
                # For new emails (same day)
                prompt = f"""
You are a professional email assistant. Generate a polite and professional response to the following email that was received today.

Original Email:
From: {email.sender}
Subject: {email.subject}
Received: {email.received_date.strftime('%Y-%m-%d %H:%M')}

Content:
{email.body}

Please generate a response that:
1. Acknowledges the email promptly
2. Addresses any questions or concerns raised in the original email
3. Maintains a professional and courteous tone
4. Is concise but comprehensive
5. Includes a proper greeting and closing

Response:
"""
            else:
                # For older emails (1-4 days old)
                prompt = f"""
You are a professional email assistant. Generate a polite and professional response to the following email that was received {days_old} days ago.

Original Email:
From: {email.sender}
Subject: {email.subject}
Received: {email.received_date.strftime('%Y-%m-%d %H:%M')}
Age: {days_old} days old

Content:
{email.body}

Please generate a response that:
1. Acknowledges the delay in responding (since the email is {days_old} days old)
2. Apologizes for the late response
3. Addresses any questions or concerns raised in the original email
4. Maintains a professional and courteous tone
5. Is concise but comprehensive
6. Includes a proper greeting and closing

Response:
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional email assistant that writes clear, polite, and professional email responses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            draft_response = response.choices[0].message.content.strip()
            logger.info(f"Generated response for {days_old}-day-old email: {email.subject}")
            return draft_response
            
        except Exception as e:
            logger.error(f"Error generating draft response: {str(e)}")
            return None

class OutlookOpenAIIntegration:
    """Main integration class for serverless deployment."""
    
    def __init__(self):
        self.graph_api = MicrosoftGraphAPI()
        self.openai_handler = OpenAIHandler()
        self.days_threshold = int(os.getenv('DAYS_THRESHOLD', 4))
        
    def process_emails(self) -> Dict:
        """Main method to process emails and generate drafts."""
        result = {
            "success": False,
            "processed_count": 0,
            "errors": [],
            "message": ""
        }
        
        try:
            logger.info("Starting email processing cycle")
            
            # Authenticate with Microsoft Graph API
            if not self.graph_api.authenticate():
                result["message"] = "Failed to authenticate with Microsoft Graph API"
                return result
            
            # Get emails needing replies
            emails = self.graph_api.get_emails_needing_replies(days_threshold=self.days_threshold)
            
            if not emails:
                result["success"] = True
                result["message"] = "No emails found needing replies"
                return result
            
            processed_count = 0
            for email in emails:
                try:
                    # Check if email should be processed
                    if not self.openai_handler.should_process_email(email):
                        logger.info(f"Skipping email from {email.sender} (domain not in allowed list)")
                        continue
                    
                    # Generate draft response
                    draft_response = self.openai_handler.generate_draft_response(email)
                    
                    if draft_response:
                        # Create draft
                        subject = f"Re: {email.subject}"
                        success = self.graph_api.create_draft(
                            subject=subject,
                            body=draft_response,
                            to_recipients=[email.sender],
                            reply_to_id=email.id
                        )
                        
                        if success:
                            processed_count += 1
                            logger.info(f"Successfully processed email: {email.subject}")
                        else:
                            result["errors"].append(f"Failed to create draft for email: {email.subject}")
                    else:
                        result["errors"].append(f"Failed to generate draft response for email: {email.subject}")
                        
                except Exception as e:
                    error_msg = f"Error processing email {email.id}: {str(e)}"
                    logger.error(error_msg)
                    result["errors"].append(error_msg)
                    continue
            
            result["success"] = True
            result["processed_count"] = processed_count
            result["message"] = f"Email processing cycle completed. Processed {processed_count} emails."
            
        except Exception as e:
            error_msg = f"Error in email processing cycle: {str(e)}"
            logger.error(error_msg)
            result["message"] = error_msg
        
        return result

# Global integration instance
integration = OutlookOpenAIIntegration()

class RequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Vercel serverless function."""
    
    def do_GET(self):
        """Handle GET requests (for testing)."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        result = integration.process_emails()
        self.wfile.write(json.dumps(result, default=str).encode())
    
    def do_POST(self):
        """Handle POST requests (for cron jobs)."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        result = integration.process_emails()
        self.wfile.write(json.dumps(result, default=str).encode())

# Vercel serverless function entry point
def handler(request, context):
    """Main handler for Vercel serverless function."""
    if request.method == 'GET':
        result = integration.process_emails()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result, default=str)
        }
    else:
        result = integration.process_emails()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result, default=str)
        } 