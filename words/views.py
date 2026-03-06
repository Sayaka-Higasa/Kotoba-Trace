from django.shortcuts import render

# Create your views here.
def word_list(request):
    return render(request, "words/list.html")