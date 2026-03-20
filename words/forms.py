from django import forms 
from .models import Word

class  WordForm(forms.ModelForm):
    is_public = forms.BooleanField(
        required=False, 
        initial=True, 
        label="公開する"
    )

    class Meta:
        model = Word
        fields = ["content", "source_type", "source_title", "source_creator",
        "memo", "is_public" ]

    def clean_is_public(self):
        data = self.cleaned_data.get('is_public')
        return 1 if data else 0