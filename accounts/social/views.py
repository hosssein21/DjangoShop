from django.shortcuts import redirect, HttpResponse
from .google_oauth import GoogleSocialAuth
from django.contrib.auth import get_user_model,login
from django.utils.crypto import get_random_string

User = get_user_model()
google_social_auth = GoogleSocialAuth()

def google_login(request):
    return redirect(google_social_auth.get_auth_url())

def google_callback(request):
    code = request.GET.get('code')
    if code:
        token_info = google_social_auth.exchange_code_for_token(code)
        if 'access_token' in token_info:
            user_info = google_social_auth.get_user_info(token_info['access_token'])
            if 'email' in user_info:
                user = User.objects.filter(email=user_info['email']).first()
                if user:
                    login(request, user)
                else:
                    random_password = get_random_string(length=15)
                    user = User.objects.create_user(email=user_info['email'], password=random_password)
                    login(request, user)
                return redirect("/")
            else:
                return HttpResponse("Email not found in user information.", status=400)
        else:
            return HttpResponse("Error occurred while fetching access token.", status=400)
    else:
        return HttpResponse("Authorization code not found in the request.", status=400)