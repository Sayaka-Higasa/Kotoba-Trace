from django.shortcuts import render

# Create your views here.
def word_list(request):
    return render(request, "words/list.html")

def word_record(request):
    return render(request, "words/record.html")

def word_record(request):
    if request.method == "POST":
        return render(request, "words/record.html", {"message": "保存が完了しました！"})