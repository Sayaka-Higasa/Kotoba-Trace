from django import forms
from django.contrib.auth. forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label = "メールアドレス")

    class Meta:
        model = User
        fields = ("username" , "email" , "password1" , "password2")

    #メアド重複チェック
    def clean_email(self):
        email = self. cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


  