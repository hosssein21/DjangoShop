from django.contrib.auth import views as auth_view
from .forms import AuthenticationForm,SignUpForm
from django.urls import reverse_lazy
from django.views import generic



class LoginView(auth_view.LoginView):
    
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
class LogoutView(auth_view.LogoutView):
    pass


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'


