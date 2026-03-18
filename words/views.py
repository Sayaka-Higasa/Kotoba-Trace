from django.shortcuts import render, get_object_or_404, redirect
from .models import Word, Tag
from .forms import WordForm
from django.core.paginator import Paginator

# --- 一覧ページ (10個ずつ表示) ---
def word_list(request):
    if request. user.is_authenticated:
    # 最新順に並び替え
        words_all = Word.objects.filter(user=request.user).order_by("-created_at")
    else:
        words_all = Word.objects.none()
    
    # 1ページ10個に設定
    paginator = Paginator(words_all, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # テンプレートへ渡す変数名を page_obj に統一
    return render(request, "words/list.html", {"page_obj": page_obj})


# --- 記録ページ (表示と保存を1つに統合) ---
def word_record(request):
    if request.method == "POST":
        # 保存処理を実行
        word = Word.objects.create(
            user = request.user,
            content = request.POST.get("content"),
            source_type = request.POST.get("source_type"),
            source_title = request.POST.get("source_title"),
            source_creator = request.POST.get("source_creator"),
            memo = request.POST.get("memo"),
            is_public = request.POST.get("is_public") == "on"
        )
        
        tags_text = request.POST.get("tags")
        if tags_text:
            tags = tags_text.split()
            for tag_name in tags:
                # データベース保存前に # を削る（##表示対策）
                clean_name = tag_name.lstrip('#')
                if clean_name:
                    tag, created = Tag.objects.get_or_create(name=clean_name)
                    word.tags.add(tag)

        return render(request, "words/record.html", {"message": "保存が完了しました！"})
    
    # POSTではない(ただページを開いた)場合は、入力フォームを表示
    return render(request, "words/record.html")


# --- 詳細ページ ---
def word_detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    return render(request, "words/detail.html", {"word": word})


# --- 編集ページ ---
def word_edit(request, word_id):
    word = get_object_or_404(Word, id=word_id)

    if request.method == "POST":
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            word = form.save()
            
            # タグの更新処理
            tags_text = request.POST.get("tags", "")
            tag_names = tags_text.split()

            word.tags.clear() # 一旦リセット
            for name in tag_names:
                clean_name = name.lstrip('#')
                if clean_name:
                    tag, _ = Tag.objects.get_or_create(name=clean_name)
                    word.tags.add(tag)
                    
            return redirect("words:word_detail", word_id=word.id)
    else:
        form = WordForm(instance=word)

    # 編集画面の初期値として、既存のタグに # をつけて表示
    tags_str = " ".join([f"#{tag.name}" for tag in word.tags.all()])

    return render(
        request,
        "words/edit.html",
        {"form": form, "tags_str": tags_str, "word": word}
    )

# words/views.py の一番下へ

def word_delete(request, word_id):
    # 自分の投稿だけを削除できるように取得（セキュリティ対策）
    word = get_object_or_404(Word, id=word_id, user=request.user)
    
    if request.method == "POST":
        word.delete()
        # 削除が終わったら一覧画面へ戻る
        return redirect("words:word_list")
    
    # POST以外（URL直接入力など）で来たら、詳細画面に戻す安全策
    return redirect("words:word_detail", word_id=word_id)