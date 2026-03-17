from django.shortcuts import render, redirect
from django.contrib. auth. forms import AuthenticationForm
from django.contrib. auth import authenticate
from django. contrib. auth. models import User
from django import forms
from django.contrib.auth import login
from .forms import SignUpForm
from django . utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from.models import PasswordReset
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django .contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages


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

#メアド入力、メール送信
def password_reset_request(request):

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            reset = PasswordReset.objects.create(
                user = user,
                password_expiry = timezone.now() + timedelta(hours = 24)
            )

            reset_link = f"http://127.0.0.1:8000/accounts/reset/{reset.password_token}/"

            send_mail(
                "パスワード再設定のご案内",
                f"""このメールはパスワードをリセットされたお客様に自動送信されています。
以下のURLをクリックし、24時間以内にパスワード再設定手続きにお進みください。

{reset_link}

※このメールに心当たりがない場合は破棄してください。
""",
            None,
            [email],
        )
        except User.DoesNotExist:
            pass  # 存在しなくても何もせず「送信しました」画面にする

        # POSTなら必ず「送信しました」画面に飛ばす
        return render(request, "accounts/password_reset_sent.html")

    # GETのときはメール入力フォームを表示
    return render(request, "accounts/password_reset_request.html") 
    
    
    
def password_reset_confirm(request,token):
    try:
        reset = PasswordReset.objects.get(password_token=token)
    except PasswordReset.DoesNotExist:
        return render(request, "accounts/invalid_link.html")
    
    #期限チェック
    if reset.password_expiry < timezone.now():
        return render(request, "accounts/expired.html")
    
    #使用済みチェック
    if reset.is_used:
        return render(request, "accounts/used.html")
    
    if request.method == "POST":
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        #パスワード一致チェック
        if password != password_confirm:
            return render(
                request,
                "accounts/password_reset_confirm.html",
                {"error":"パスワードが一致しません"}
            )
        try:
            validate_password(password, user=reset.user)
        except ValidationError as e:
            return render(
                 request,
                "accounts/password_reset_confirm.html",
                {"error": e.messages[0]}
            )
           
        user = reset.user
        user.set_password(password)
        user.save()

        reset.is_used = True
        reset.save()

        return redirect("accounts:login")
    
    return render(request,"accounts/password_reset_confirm.html")

#設定画面
@login_required
def settings_view(request):
    return render(request,"accounts/settings.html")

#メアド変更（設定画面）
@login_required
def email_change(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if User.objects.filter(email=email).exclude(id.request.user.id).exists():
            messages.error(request,"このメールアドレスは既に登録されています")
            return redirect("email_change")
        
        request.user.email = email
        request.user.save()

        return redirect("settings")
    return render (request,"accounts/email_change.html")


