import os
import pickle
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from django.core.exceptions import ValidationError
from django.conf import settings
from email.mime.text import MIMEText
import base64
import logging

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Get Gmail credentials from token file."""
    print("Getting Gmail credentials")  # Print for immediate feedback
    logger.debug("Getting Gmail credentials")
    
    token_path = os.path.join(settings.BASE_DIR, 'token.pickle')
    credentials_path = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_FILE
    
    print(f"Token path: {token_path}")  # Print file paths
    print(f"Credentials path: {credentials_path}")
    
    if not os.path.exists(credentials_path):
        print("credentials.json not found")
        logger.error("credentials.json not found")
        raise ValidationError("Gmail credentials file not found. Please check your configuration.")
        
    if not os.path.exists(token_path):
        print("token.pickle not found")
        logger.error("token.pickle not found")
        raise ValidationError("Gmail authentication token not found. Please run setup_gmail_oauth command.")
    
    try:
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            print("Loaded credentials from token.pickle")
            logger.debug("Loaded credentials from token.pickle")
    except Exception as e:
        print(f"Error loading token.pickle: {str(e)}")
        logger.error(f"Error loading token.pickle: {str(e)}", exc_info=True)
        raise ValidationError("Error loading Gmail credentials. Please run setup_gmail_oauth command.")
    
    if not creds or not creds.valid:
        print("Credentials need refresh")
        logger.debug("Credentials need refresh")
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Attempting to refresh credentials")
                logger.debug("Attempting to refresh credentials")
                creds.refresh(Request())
                print("Successfully refreshed credentials")
                logger.info("Successfully refreshed credentials")
            except Exception as e:
                print(f"Error refreshing credentials: {str(e)}")
                logger.error(f"Error refreshing credentials: {str(e)}", exc_info=True)
                raise ValidationError("Error refreshing Gmail credentials. Please run setup_gmail_oauth command.")
        else:
            print("Invalid credentials")
            logger.error("Invalid credentials")
            raise ValidationError("Invalid Gmail credentials. Please run setup_gmail_oauth command.")
            
        # Save the refreshed credentials
        try:
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
                print("Saved refreshed credentials")
                logger.debug("Saved refreshed credentials")
        except Exception as e:
            print(f"Error saving refreshed credentials: {str(e)}")
            logger.error(f"Error saving refreshed credentials: {str(e)}", exc_info=True)
            # Don't raise here as we still have valid credentials in memory
    
    return creds

def create_message(sender, to, subject, message_text, html_message=None):
    """Create a message for an email."""
    print(f"Creating email message - From: {sender}, To: {to}, Subject: {subject}")
    logger.debug(f"Creating email message - From: {sender}, To: {to}, Subject: {subject}")
    
    if html_message:
        msg = MIMEText(html_message, 'html')
    else:
        msg = MIMEText(message_text, 'plain')
        
    msg['to'] = to
    msg['from'] = sender
    msg['subject'] = subject
    
    print("Email message created successfully")
    logger.debug("Email message created successfully")
    return msg
