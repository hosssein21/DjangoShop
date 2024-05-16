
from abc import ABC, abstractmethod
from django.conf import settings

class SocialAuthBase(ABC):
    provider_name = None
    client_id = None
    client_secret = None
    redirect_uri = None
    scope = None

    @abstractmethod
    def get_auth_url(self):
        pass

    @abstractmethod
    def exchange_code_for_token(self, code):
        pass

    @abstractmethod
    def get_user_info(self, access_token):
        pass

def get_domain():
    from django.contrib.sites.models import Site
    return Site.objects.get_current().domain


def get_protocol():
    return'https' if getattr(settings, 'SECURE_SSL_REDIRECT', False) else 'http'


