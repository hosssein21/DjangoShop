from django.urls import path,include
from . import views

app_name = 'accounts'
urlpatterns = [
    #base url for authentication
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
     path('signup/', views.SignUpView.as_view(), name='signup'),
     
     #social accounts authentication
    path('socials/google/',include('accounts.social.urls')),
    
    #sending email
    path('send-test/',views.TestEmailView.as_view(),name='send_test'),
    
    #forgot-password
    path('password-reset/',views.ResetPasswordView.as_view(),name='password_reset'),
    path('password-reset-done/',views.PasswordRestDoneView.as_view(),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',views.PasswordRestConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
    
]
