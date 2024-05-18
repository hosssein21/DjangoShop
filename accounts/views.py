from django.contrib.auth import views as auth_view
from .forms import AuthenticationForm,SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from mail_templated import send_mail
from django.http import HttpResponse



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


class TestEmailView(View):
    
    def get(self,request,*args,**kwargs):
        send_mail('email/hello.tpl', {'name': 'developer'},'admin@admin.com' , ['hossein@gmail.com'])
        return HttpResponse('email sent successfully')
    
    


