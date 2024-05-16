from .base import SocialAuthBase,get_domain,get_protocol
from .app_settings import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET
import requests

class GoogleSocialAuth(SocialAuthBase):
    provider_name = 'google'
    client_id = GOOGLE_CLIENT_ID
    client_secret = GOOGLE_CLIENT_SECRET
    redirect_uri = "http://127.0.0.1:8000/accounts/socials/google/callback" 
    scope = 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
    timeout = 5  # Set timeout value in seconds

    def get_auth_url(self):
        auth_url = 'https://accounts.google.com/o/oauth2/auth'
        print(self.redirect_uri)
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': self.scope,
        }
        return auth_url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])

    def exchange_code_for_token(self, code):
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code',
        }
        try:
            response = requests.post(token_url, data=token_data, timeout=self.timeout)
            return response.json()
        except requests.Timeout:
            # Handle timeout error
            print("Token exchange request timed out.")
            return None
        except requests.RequestException as e:
            # Handle other request errors
            print("An error occurred:", e)
            return None

    def get_user_info(self, access_token):
        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        try:
            response = requests.get(user_info_url, headers=headers, timeout=self.timeout)
            return response.json()
        except requests.Timeout:
            # Handle timeout error
            print("User info request timed out.")
            return None
        except requests.RequestException as e:
            # Handle other request errors
            print("An error occurred:", e)
            return None
        
