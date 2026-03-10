from django.urls import path 
from . import views

app_name = "words"
urlpatterns = [
    path("",views.word_list, name= "word_list") , #一覧ページ
    path("words/record",views.word_record,name="word_record"), #記録ページ
    path("<int:word_id>/", views.word_detail,name="word_detail"), #詳細
]

