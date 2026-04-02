from django import forms
from django.contrib.auth. forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class SignUpForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Django標準のパスワードチェックを無効化する（自分のcleanメソッドでやるため）
        if 'password1' in self.fields:
            self.fields['password1'].validators = []
        if 'password2' in self.fields:
            self.fields['password2'].validators = []

    def _post_clean(self):
        pass

    class Meta:
        model = User
        fields = ("name", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        return email

    def clean_password1(self):
        p1 = self.cleaned_data.get("password1")
        errors = []
        if p1:
            if not any(c.isalpha() for c in p1):
                errors.append("パスワードには英字を含めてください")
            if not any(c.isdigit() for c in p1):
                errors.append("パスワードには数字を含めてください")
            if len(p1) < 10:
                errors.append("パスワードは10文字以上で入力してください")
        
        if errors:
            raise forms.ValidationError(errors)
        return p1
    def clean(self):
        cleaned_data = self.cleaned_data
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "パスワードが一致しません")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data["name"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
  


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].validators = []
        self.fields['new_password2'].validators = []

    def clean_new_password1(self):
        p1 = self.cleaned_data.get("new_password1")
        errors = []

        if p1:
            if not any(c.isalpha() for c in p1) or not any(c.isdigit() for c in p1):
                errors.append("パスワードには英字と数字の両方を含めてください")
            if len(p1) < 10:
                errors.append("パスワードは10文字以上で入力してください")

        if errors:
            raise forms.ValidationError(errors)

        return p1

    def clean_new_password2(self):
        p1 = self.cleaned_data.get('new_password1')
        p2 = self.cleaned_data.get('new_password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError(_("パスワードが一致していません。"))
        return p2

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={'autofocus': True})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(self.request, username=email, password=password)
            if user is None:
                raise forms.ValidationError("メールアドレスまたはパスワードが間違っています")

        return cleaned_data

class MySetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="新しいパスワード",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'autofocus': True}),
        strip=False,
    )
    password2 = forms.CharField(
        label="新しいパスワード（確認）",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    def clean_password1(self):
        p1 = self.cleaned_data.get("password1")
        errors = []
        if p1:
            if not any(c.isalpha() for c in p1):
                errors.append("パスワードには英字を含めてください")
            if not any(c.isdigit() for c in p1):
                errors.append("パスワードには数字を含めてください")
            if len(p1) < 10:
                errors.append("パスワードは10文字以上で入力してください")
        
        if errors:
            raise forms.ValidationError(errors)
        return p1

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "パスワードが一致しません")
        return cleaned_data
