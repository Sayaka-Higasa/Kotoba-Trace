from django.urls import path 
from django.contrib.auth import views as auth_views
from .views import EmailLoginForm, signup_view
from . import views

app_name = "accounts"
urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=EmailLoginForm
        ),
        name="login"
    ),
    path("logout/" , auth_views.LogoutView.as_view(), name = "logout"),
    path("signup/", signup_view, name="signup") ,#新規登録 
    #パスワードリセット関連
    path("password_reset/" , views.password_reset_request , name = "password_reset"),
    path("reset/<uuid:token>/", views.password_reset_confirm, name= "password_reset_confirm"),
]