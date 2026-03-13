from django.shortcuts import render
from django.contrib. auth. forms import AuthenticationForm
from django.contrib. auth import authenticate
from django. contrib. auth. models import User
from django import forms

# Create your views here.
class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    def clean(self):
        email = self. cleaned_data.get("username")
        password = self. cleaned_data.get( "password")
        if email and password :
            try:
                user_obj = User.objects.get("email=email")
            except User.DoesNotExist:
                raise forms.ValidationError("メールアドレスが存在しません")
            self.user_cache = authenticate(username=user_obj.username, password = password)
            if self.user_cache is None:
                raise forms.ValidationError("パスワードが間違っています")
        return self.cleaned_data