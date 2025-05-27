from django.core.management.base import BaseCommand
from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sets up Gmail OAuth2 authentication'

    def handle(self, *args, **options):
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        token_path = os.path.join(settings.BASE_DIR, 'token.pickle')
        
        # Ensure the token file exists and is writable
        if not os.path.exists(token_path):
            with open(token_path, 'wb') as f:
                pickle.dump(None, f)
        
        try:
            # Check if we have valid credentials
            if os.path.exists(token_path):
                with open(token_path, 'rb') as token:
                    try:
                        creds = pickle.load(token)
                        if creds and not creds.expired:
                            self.stdout.write(self.style.SUCCESS('OAuth token already exists and is valid'))
                            return
                    except Exception:
                        pass  # Continue with new token creation if existing token is invalid
            
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_OAUTH2_CLIENT_SECRETS_FILE,
                SCOPES,
                redirect_uri='http://localhost:80/oauth2callback'
            )
            
            # Get the authorization URL
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            self.stdout.write(self.style.WARNING(
                '\nPlease visit this URL to authorize the application:\n\n'
                f'{auth_url}\n\n'
                'After authorization, you will be redirected to localhost. Copy the "code" parameter from the URL.'
            ))
            
            code = input('Enter the authorization code: ').strip()
            
            # Exchange code for credentials
            flow.fetch_token(code=code)
            creds = flow.credentials
            
            # Save credentials
            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            
            self.stdout.write(self.style.SUCCESS('Successfully set up Gmail OAuth2 authentication'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error setting up OAuth: {str(e)}'))
            raise
