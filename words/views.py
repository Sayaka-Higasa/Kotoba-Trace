from django.shortcuts import render
from. models import Word

# 一覧ページ閲覧リクエストがきたら、表示できる形に変換して返す
def word_list(request):
    return render(request, "words/list.html")

#記録ページ閲覧リクエストがきたら、表示できる形に変換して返す
def word_record(request):
    return render(request, "words/record.html")

#記録ページで入力した情報を保存
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

#記録した言葉を一覧ページに表示
def word_list(request):
    words = Word.objects.all()
    return render (request, "words/list.html" , {"words" : words})