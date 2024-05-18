from django.contrib.auth import views as auth_view
from .forms import AuthenticationForm,SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from .utils import EmailThread,TemplateEmailThread
from mail_templated import EmailMessage
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model





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
    

class ResetPasswordView(auth_view.PasswordResetView):
    template_name = 'email/password-reset.html'
    email_template_name = 'email/password-reset-email.html'
    subject_template_name = 'email/password-reset-subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    token_generator = default_token_generator
    
    
    def form_valid(self, form):
        """
        If the form is valid, send the email using threading.
        """
        User = get_user_model()
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # If user does not exist, silently ignore to avoid leaking information
            return super().form_valid(form)

        c = {
            'email': user.email,
            'domain': self.request.META['HTTP_HOST'],
            'site_name': 'Django Shop',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http' if not self.request.is_secure() else 'https',
        }
        subject = render_to_string(self.subject_template_name, c)
        subject = ''.join(subject.splitlines())
        html_message = render_to_string(self.email_template_name, c)
        plain_message = strip_tags(html_message)
        from_email = 'parto@gmail.com'
        recipient_list = [user.email]

        # Start a new thread for sending the email
        TemplateEmailThread(subject, html_message, plain_message, from_email, recipient_list).start()
        
        return super().form_valid(form)
    
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Do nothing. Override this method to prevent Django from sending the email immediately.
        """
        pass
    
    
    
class PasswordRestDoneView(auth_view.PasswordResetDoneView):
    template_name="email/password-reset-done.html"
    

class PasswordRestConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'email/password-reset-confirm.html'
    success_url = reverse_lazy("accounts:password_reset_complete")
    
class PasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'email/password-reset-complete.html'
    
    
    
    