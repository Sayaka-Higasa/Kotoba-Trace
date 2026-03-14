from django import forms
from django.contrib.auth. forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label = "メールアドレス")
    password1 = forms.CharField(
        label = "パスワード",
        widget = forms.PasswordInput,
        strip=False
    )
    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username" , "email" , "password1" , "password2")

    #メアド重複チェック
    def clean_email(self):
        email = self. cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        return email
    
    #英数字の両方を含むかチェック
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        has_letter = any(char.isalpha() for char in password)
        has_digit = any(char.isdigit() for char in password)

        if not (has_letter and has_digit):
            raise forms.ValidationError("パスワードは10文字以上で、英字と数字の両方を含めてください")
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


  