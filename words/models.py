from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Word(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.CharField(max_length= 300) #ことば
    source_type = models.CharField(max_length= 20) #出典
    source_title = models.CharField(max_length= 100 , blank = True) #タイトル
    source_creator = models.CharField(max_length= 100 , blank = True) #著者、アーティスト
    memo = models.CharField(max_length= 500 , blank = True) #メモ
    is_public = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField("Tag" , blank = True)

#タグテーブル
class Tag(models.Model):
    name = models.CharField(max_length= 50) #タグ名
    def __str__(self):
        return self.name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)