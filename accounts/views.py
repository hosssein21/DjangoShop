from django.contrib.auth import views as auth_view
from .forms import AuthenticationForm,SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from .utils import EmailThread,TemplateEmailThread
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from .tasks import send_password_reset_email

User=get_user_model()


class LoginView(auth_view.LoginView):
    
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
class LogoutView(auth_view.LogoutView):
    pass


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:account_activation_sent')
    template_name = 'accounts/signup.html'
    
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_verified = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        message = render_to_string('email/account-activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email = EmailMessage(subject, message, to=[user.email])
        email.content_subtype = 'html'  # Specify that the email content is HTML
        email.send()
        return super().form_valid(form)

class ActivateView(generic.View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'email/account-activation-invalid.html')


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
        
        # Use Celery to send the email
        # send_password_reset_email.delay(subject, plain_message, html_message, from_email, recipient_list)
        
        
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
    
    
    
    