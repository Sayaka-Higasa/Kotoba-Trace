from django import forms
from django.contrib.auth. forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

User = get_user_model()

class SignUpForm(UserCreationForm):
    name = forms.CharField(label="ユーザー名", max_length=50, required=True)
    email = forms.EmailField(required=True, label="メールアドレス")
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        strip=False
    )
    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = ("name", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1:
            has_letter = any(char.isalpha() for char in p1)
            has_digit = any(char.isdigit() for char in p1)
            # 英字と数字両方が揃ってない場合にエラー
            if not (has_letter and has_digit):
                raise forms.ValidationError("パスワードには英字と数字の両方を含めてください")
            if len(p1) < 10:
                raise forms.ValidationError("パスワードは10文字以上で入力してください")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("パスワードが一致しません")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data["name"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
  
from django.contrib.auth.forms import PasswordChangeForm

class MyPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        p1 = self.cleaned_data.get("new_password1")
        if p1:
            has_letter = any(c.isalpha() for c in p1)
            has_digit = any(c.isdigit() for c in p1)
            if not (has_letter and has_digit):
                raise forms.ValidationError("パスワードには英字と数字の両方を含めてください")
            if len(p1) < 10:
                raise forms.ValidationError("パスワードは10文字以上で入力してください")
        return p1

class CustomAuthenticationForm(AuthenticationForm):
  
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')  
        password = cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                self.add_error('username', "メールアドレスまたはパスワードが間違っています")
                self.add_error('password', "メールアドレスまたはパスワードが間違っています")

        return cleaned_data

class LoginForm(AuthenticationForm):
    userbame = forms.EmailField(
        label="メールアドレス",
        widget = forms.EmailInput(attrs={
            "class": "form-control",
        })
    )

    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        })
    )