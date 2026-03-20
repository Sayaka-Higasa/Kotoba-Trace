from django.db import models
from django.conf import settings

# Word モデル
class Word(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    source_type = models.CharField(max_length=20)
    source_title = models.CharField(max_length=100, blank=True)
    source_creator = models.CharField(max_length=100, blank=True)
    memo = models.CharField(max_length=500, blank=True)
    is_public = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField("Tag", through="WordTag", blank=True)

# Tag モデル
class Tag(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 中間テーブル（WordTag）
class WordTag(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("word", "tag")