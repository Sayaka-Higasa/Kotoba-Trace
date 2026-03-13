from django.urls import path 
from django . contrib.auth import views as auth_views
from .views import EmailLoginForm

app_name = "accounts"
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name = "accounts/login.html"), name= "login") , #ログインページ
    path("logout/" , auth_views.LogoutView.as_view(), name = "logout"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=EmailLoginForm
        ),
        name="login"
    ),
    ]