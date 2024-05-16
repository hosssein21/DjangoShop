from django.contrib.auth import forms as auth_form
from django import forms
from django.contrib.auth import get_user_model

User=get_user_model()

class AuthenticationForm(auth_form.AuthenticationForm):
    
   def confirm_login_allowed(self, user):
    super(AuthenticationForm,self).confirm_login_allowed(user)
        
        # if not user.is_verified:
        #     raise ValidationError("user is not verified")
        
class SignUpForm(auth_form.UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        
        
        