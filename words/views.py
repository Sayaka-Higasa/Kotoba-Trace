from django.shortcuts import render
from. models import Word

# Create your views here.
def word_list(request):
    return render(request, "words/list.html")

def word_record(request):
    return render(request, "words/record.html")

def word_record(request):
    if request.method == "POST":
        Word.objects.create(
            user = request.user,
            content = request.POST.get("content"),
            source_type = request.POST.get("source_type"),
            source_title = request.POST.get("source_title"),
            source_creator = request.POST.get("source_creator"),
            memo = request.POST.get("memo"),
            is_public = request.POST.get("is_public") =="on"
        )

        return render(request, "words/record.html", {"message": "保存が完了しました！"})
    return render(request , "words/record.html")