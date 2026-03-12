from django.shortcuts import render , get_object_or_404, redirect
from. models import Word , Tag
from .forms import WordForm


# 一覧ページ閲覧リクエストがきたら、表示できる形に変換して返す
def word_list(request):
    return render(request, "words/list.html")

#記録ページ閲覧リクエストがきたら、表示できる形に変換して返す
def word_record(request):
    return render(request, "words/record.html")

#記録ページで入力した情報を保存
def word_record(request):
    if request.method == "POST":
       word = Word.objects.create(
            user = request.user,
            content = request.POST.get("content"),
            source_type = request.POST.get("source_type"),
            source_title = request.POST.get("source_title"),
            source_creator = request.POST.get("source_creator"),
            memo = request.POST.get("memo"),
            is_public = request.POST.get("is_public") =="on"
        )
       
       tags_text = request.POST.get("tags")

       if tags_text:
           tags = tags_text.split()
           
           for tag_name in tags:
               tag, created = Tag.objects.get_or_create (name = tag_name)
               word.tags.add (tag)

    return render(request, "words/record.html", {"message": "保存が完了しました！"})
    

#記録した言葉を一覧ページに表示
def word_list(request):
    words = Word.objects.all()
    return render (request, "words/list.html" , {"words" : words})

#言葉一覧で言葉をクリックしたときに詳細を返す
def word_detail(request , word_id):
    word = get_object_or_404 (Word , pk = word_id)
    return render (request , "words/detail.html" , {"word" : word })

#言葉詳細で編集ボタン押したときに編集画面を返す
def word_edit(request , word_id):
    word = get_object_or_404(Word, id = word_id)
   
    if request.method == "POST":
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect("words:word_detail" , word_id = word.id)
    else:
        form = WordForm(instance=word)
        tags_str = " ".join([tag.name for tag in word.tags.all()])

        return render(request, "words/edit.html" , {"form": form, "tags_str": tags_str})