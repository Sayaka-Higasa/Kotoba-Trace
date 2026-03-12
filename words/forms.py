from django import forms 
from .models import Word

class  WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ["content", "source_type", "source_title", "source_creator",
        "memo", "is_public", "tags"]