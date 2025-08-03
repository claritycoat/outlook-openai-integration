#!/usr/bin/env python3
"""
Outlook-OpenAI Integration
Automatically scans Outlook emails and generates draft responses using OpenAI.
"""

import os
import json
import time
import schedule
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

import requests
import msal
from openai import OpenAI
from dateutil import parser

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('outlook_openai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Email:
    id: str
    subject: str
    sender: str
    body: str
    received_date: datetime
    is_read: bool

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
    
    def get_emails(self, folder: str = "Inbox", max_count: int = 10, unread_only: bool = False) -> List[Email]:
        """Retrieve emails from specified folder."""
        try:
            filter_query = "$filter=isRead eq false" if unread_only else ""
            select_query = "$select=id,subject,from,body,receivedDateTime,isRead"
            top_query = f"$top={max_count}"
            
            query_params = "&".join([filter_query, select_query, top_query]) if filter_query else "&".join([select_query, top_query])
            
            url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder}/messages?{query_params}&$orderby=receivedDateTime desc"
            
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            
            emails = []
            for item in response.json().get("value", []):
                email = Email(
                    id=item["id"],
                    subject=item.get("subject", "No Subject"),
                    sender=item["from"]["emailAddress"]["address"],
                    body=item["body"]["content"],
                    received_date=parser.parse(item["receivedDateTime"]),
                    is_read=item["isRead"]
                )
                emails.append(email)
            
            logger.info(f"Retrieved {len(emails)} emails from {folder}")
            return emails
            
        except Exception as e:
            logger.error(f"Error retrieving emails: {str(e)}")
            return []
    
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
    
    def mark_as_read(self, email_id: str) -> bool:
        """Mark an email as read."""
        try:
            url = f"https://graph.microsoft.com/v1.0/me/messages/{email_id}"
            data = {"isRead": True}
            response = requests.patch(url, headers=self._get_headers(), json=data)
            response.raise_for_status()
            
            logger.info(f"Marked email {email_id} as read")
            return True
            
        except Exception as e:
            logger.error(f"Error marking email as read: {str(e)}")
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
        """Generate a draft response using OpenAI."""
        try:
            prompt = f"""
You are a professional email assistant. Generate a polite and professional response to the following email.

Original Email:
From: {email.sender}
Subject: {email.subject}
Received: {email.received_date}

Content:
{email.body}

Please generate a response that:
1. Acknowledges the sender's message
2. Addresses any questions or concerns raised
3. Maintains a professional and courteous tone
4. Is concise but comprehensive
5. Includes a proper greeting and closing

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
            logger.info(f"Generated draft response for email: {email.subject}")
            return draft_response
            
        except Exception as e:
            logger.error(f"Error generating draft response: {str(e)}")
            return None

class OutlookOpenAIIntegration:
    """Main integration class that orchestrates email scanning and draft generation."""
    
    def __init__(self):
        self.graph_api = MicrosoftGraphAPI()
        self.openai_handler = OpenAIHandler()
        self.email_folder = os.getenv('EMAIL_FOLDER', 'Inbox')
        self.processed_folder = os.getenv('PROCESSED_FOLDER', 'Drafts')
        self.max_emails = int(os.getenv('MAX_EMAILS_PER_SCAN', 10))
        
    def process_emails(self):
        """Main method to process emails and generate drafts."""
        try:
            logger.info("Starting email processing cycle")
            
            # Authenticate with Microsoft Graph API
            if not self.graph_api.authenticate():
                logger.error("Failed to authenticate. Skipping this cycle.")
                return
            
            # Get unread emails
            emails = self.graph_api.get_emails(
                folder=self.email_folder,
                max_count=self.max_emails,
                unread_only=True
            )
            
            if not emails:
                logger.info("No new emails to process")
                return
            
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
                            # Mark original email as read
                            self.graph_api.mark_as_read(email.id)
                            processed_count += 1
                            logger.info(f"Successfully processed email: {email.subject}")
                        else:
                            logger.error(f"Failed to create draft for email: {email.subject}")
                    else:
                        logger.warning(f"Failed to generate draft response for email: {email.subject}")
                        
                except Exception as e:
                    logger.error(f"Error processing email {email.id}: {str(e)}")
                    continue
            
            logger.info(f"Email processing cycle completed. Processed {processed_count} emails.")
            
        except Exception as e:
            logger.error(f"Error in email processing cycle: {str(e)}")
    
    def run_scheduled(self):
        """Run the integration on a schedule."""
        interval_minutes = int(os.getenv('SCAN_INTERVAL_MINUTES', 15))
        
        logger.info(f"Starting scheduled email processing (every {interval_minutes} minutes)")
        
        # Run immediately
        self.process_emails()
        
        # Schedule recurring runs
        schedule.every(interval_minutes).minutes.do(self.process_emails)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main entry point."""
    logger.info("Starting Outlook-OpenAI Integration")
    
    # Validate environment variables
    required_vars = ['CLIENT_ID', 'CLIENT_SECRET', 'TENANT_ID', 'OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.error("Please check your .env file and ensure all required variables are set.")
        return
    
    integration = OutlookOpenAIIntegration()
    
    # Run in scheduled mode
    integration.run_scheduled()

if __name__ == "__main__":
    main() 