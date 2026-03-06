from django.urls import path 
from . import views

app_name = "words"
urlpatterns = [
    path("",views.word_list, name= "word_list") 
]
