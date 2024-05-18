from django.contrib.auth import views as auth_view
from .forms import AuthenticationForm,SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from .utils import EmailThread
from mail_templated import EmailMessage
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin


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
        email_obj= EmailMessage('email/hello.tpl', {'user':'developer'}, 'hossseinkazemi79@gmail.com',
                       to=['pythonprojectkazemi@gmail.com'])
        EmailThread(email_obj).start()
        return HttpResponse('email sent successfully')
    

class ResetPasswordView(SuccessMessageMixin, auth_view.PasswordResetView):
    template_name = 'email/password-reset.html'
    email_template_name = 'email/password-reset-email.html'
    subject_template_name = 'email/password-reset-subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    
class PasswordRestDoneView(auth_view.PasswordResetDoneView):
    template_name="email/password-reset-done.html"
    

class PasswordRestConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'email/password-reset-confirm.html'
    success_url = reverse_lazy("accounts:password_reset_complete")
    
class PasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'email/password-reset-complete.html'
    
    
    
    