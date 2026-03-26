from django.urls import path 
from django.contrib.auth import views as auth_views
from .views import EmailLoginForm, signup_view
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

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

   path(
        'logout/',
        LogoutView.as_view(next_page=reverse_lazy('search:index')),
        name='logout'
    ),

    path("signup/", signup_view, name="signup") ,#新規登録 
    
    #パスワードリセット関連
    path("password_reset/" , views.password_reset_request , name = "password_reset"),
   

     #パスワード再設定完了
    path('reset/complete/', views.password_reset_complete, name='password_reset_complete'),

     path("reset/<str:token>/", views.password_reset_confirm, name="password_reset_confirm"),

    #設定画面
    path("settings/", views.settings_view,name="settings"),
    path ("email-change/",views.email_change, name="email_change"),
    path("password_change/",views.MyPasswordChangeView.as_view(),
         name = "password_change"),]