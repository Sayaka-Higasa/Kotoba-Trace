from django.urls import path 
from . import views

app_name = "words"
urlpatterns = [
    path("",views.word_list, name= "word_list") , #一覧ページ
    path("words/record",views.word_record,name="word_record"), #記録ページ
    path("<int:word_id>/", views.word_detail,name="word_detail"), #詳細
    path("edit<int:word_id>/" , views.word_edit, name="word_edit"), #編集
    path("edit<int:word_id>/delete/", views.word_delete, name="word_delete"),
    ]

