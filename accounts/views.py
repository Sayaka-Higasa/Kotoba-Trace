from django.shortcuts import render, redirect
from django.contrib. auth. forms import AuthenticationForm
from django.contrib. auth import authenticate
from django. contrib. auth. models import User
from django import forms
from django.contrib.auth import login
from .forms import SignUpForm

# ログイン
class EmailLoginForm(AuthenticationForm):
    #ユーザー名欄をメールアドレス用として定義
    username = forms.EmailField(label="Email")

    def clean(self):
        email = self. cleaned_data.get("username")
        password = self. cleaned_data.get( "password")
        if email and password :
            try:
                #メアドからユーザーを探す
                user_obj = User.objects.get(email=email)
                #見つかったユーザーのユーザー名を使って認証
                self.user_cache = authenticate(
                    self.request, 
                    username = user_obj.username,
                    password = password
                )
            except User.DoesNotExist:
                raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません")
            self.user_cache = authenticate(username=user_obj.username, password = password)
            if self.user_cache is None:
                raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません")
        return self.cleaned_data
    
    #新規登録、自動ログイン
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            #ログイン
            login(request,user)
            return redirect("/")
    else:
        form = SignUpForm()
    return render (request, "accounts/signup.html", {"form": form})