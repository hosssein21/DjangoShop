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
    path('send-test/',views.TestEmailView.as_view(),name='send_test')
    
    
]
