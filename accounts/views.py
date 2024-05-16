from django.contrib.auth import views as auth_view
from .forms import AuthenticationForm


class LoginView(auth_view.LoginView):
    
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
class LogoutView(auth_view.LogoutView):
    pass