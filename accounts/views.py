from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django import forms
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import PasswordReset
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, MyPasswordChangeForm
from .forms import MySetPasswordForm

User = get_user_model()


# ログインフォーム
class EmailLoginForm(forms.Form):
    username = forms.EmailField(label="メールアドレス", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if email and password:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(self.request, email=user_obj.email, password=password)
                if user is None:
                    raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません")
                self.user_cache = user
            except User.DoesNotExist:
                raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

# 新規登録
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(reverse("search:index"))
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

# ログイン
def login_view(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(reverse("search:index"))
    else:
        form = EmailLoginForm()
    return render(request, "accounts/login.html", {"form": form})

# パスワードリセット申請（メール送信）
def password_reset_request(request):
    reset_link = None
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        email_field = forms.EmailField()
        try:
            email_field.clean(email)
        except ValidationError:
            return render(request, "accounts/password_reset_request.html", {
                "error": "有効なメールアドレスを入力してください"
            })
        
        try:
            user = User.objects.get(email=email)
            reset = PasswordReset.objects.create(
                user=user,
                password_expiry=timezone.now() + timedelta(hours=24)
            )
            # 本番用
            reset_link = f"https://kotobatrace.pythonanywhere.com/accounts/reset/{reset.password_token}/"

            # reset_link = f"http://127.0.0.1:8000/accounts/reset/{reset.password_token}/"
            
            mail_subject= "【Kotoba Trace】パスワード再設定のご案内"
            mail_body = f"""このメールはパスワードをリセットされたお客様に自動送信されています。
以下のURLをクリックし、24時間以内にパスワード再設定手続きにお進みください。

{reset_link}

※このメールにお心当たりがないお客様はこのメールを破棄していただくようお願いいたします。"""
            
            send_mail(
                mail_subject,
                mail_body,
                None,
                [email],
            )
        
        except User.DoesNotExist:
            # ユーザーがいない場合も、reset_link は None のまま次へ進む
            pass

        return render(request, "accounts/password_reset_sent.html", {"reset_link": reset_link})


    return render(request, "accounts/password_reset_request.html")
# パスワード再設定画面（URLから飛んでくる場所）
def password_reset_confirm(request, token):
    try:
        reset = PasswordReset.objects.get(password_token=str(token))
    except PasswordReset.DoesNotExist:
        return render(request, "accounts/invalid_link.html")
    
    if reset.password_expiry < timezone.now():
        return render(request, "accounts/expired.html")
    if reset.is_used:
        return render(request, "accounts/used.html")
    
    if request.method == "POST":
            # 1. 自作フォーム(MySetPasswordForm)にデータを渡す
            form = MySetPasswordForm(request.POST)
            
            # 2. フォームのバリデーション（英数字・10文字チェック）を実行
            if form.is_valid():
                user = reset.user
                # フォームで検証済みの安全なパスワードを取り出す
                user.set_password(form.cleaned_data["password1"])
                user.save()
                
                reset.is_used = True
                reset.save()
                return redirect("accounts:password_reset_complete")
            else:
                # 3. エラーがあった場合、最初のエラー内容を1つ取得
                first_error = None
                for errors in form.errors.values():
                    first_error = errors[0]
                    break
                
                # エラーメッセージを error としてテンプレートに返して再表示
                return render(request, "accounts/password_reset_confirm.html", {"error": first_error})
        
    return render(request, "accounts/password_reset_confirm.html")

# 設定・変更系
@login_required
def settings_view(request):
    return render(request, "accounts/settings.html")

@login_required
def email_change(request):
    if request.method == "POST":
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.error(request, "このメールアドレスは既に登録されています")
                return redirect("accounts:email_change")
            request.user.email = email
            request.user.save()
            messages.success(request, "メールアドレスの変更が完了しました!")
            return redirect("accounts:settings")
    else:
        form = EmailChangeForm()
    return render(request, "accounts/email_change.html", {"form": form})

class EmailChangeForm(forms.Form):
    email = forms.EmailField(required=True)

class MyPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:settings")
    form_class = MyPasswordChangeForm
    def form_valid(self, form):
        messages.success(self.request, "パスワードの変更が完了しました!")
        return super().form_valid(form)

def password_reset_complete(request):
    return render(request, "accounts/password_reset_complete.html")