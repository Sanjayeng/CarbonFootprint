from django.urls import path
from . import views
from .views import custom_logout
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", custom_logout, name="logout"),
    path("register/", views.register, name="register"),
]

