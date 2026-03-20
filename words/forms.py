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

        labels = {
            "content": "ことば",
            "source_type": "出典",
            "source_title": "作品名・曲名",
            "source_creator": "著者・アーティスト",
            "memo": "メモ",
        }

        error_messages = {
            "source_type" : {
                "required" : "出典を入力してください"
            },
            "content" : {
                "required" : "ことばを入力してください"
            },
        }

    def clean_is_public(self):
        data = self.cleaned_data.get('is_public')
        return 1 if data else 0