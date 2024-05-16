
from django.urls import path, include
from . import views


urlpatterns = [
    path("login/",views.google_login,name="google-login"),
    path("callback/",views.google_callback,name="google-callback"),
]