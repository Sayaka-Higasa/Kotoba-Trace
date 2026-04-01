import unicodedata
from django.shortcuts import render, get_object_or_404, redirect
from .models import Word, Tag
from .forms import WordForm
from django.core.paginator import Paginator
from django.contrib import messages


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
    success_message = None

    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.user = request.user
           
            if word.content:
                word.content = unicodedata.normalize('NFKC', word.content)
            if word.source_title:
                word.source_title = unicodedata.normalize('NFKC', word.source_title)
            if word.source_creator:
                word.source_creator = unicodedata.normalize('NFKC', word.source_creator)

            word.save()

            # タグ処理
            tags_text = request.POST.get("tags", "")
            if tags_text:
                normalized = unicodedata.normalize('NFKC', tags_text).replace('　', ' ')
                prepared_text = normalized.replace('#', ' #')
                for tag_name in prepared_text.split():
                    clean_name = tag_name.lstrip('#＃')
                    if clean_name:
                        tag, _ = Tag.objects.get_or_create(name=clean_name)
                        word.tags.add(tag)

            success_message = "記録が完了しました！"
            form = WordForm()  # 入力クリア
    else:
        form = WordForm()

    return render(request, "words/record.html", {
        "form": form,
        "success_message": success_message
    })
    


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
            word = form.save(commit=False)

            if word.content:
                word.content = unicodedata.normalize('NFKC', word.content)
            if word.source_title:
                word.source_title = unicodedata.normalize('NFKC', word.source_title)
            if word.source_creator:
                word.source_creator = unicodedata.normalize('NFKC', word.source_creator)

            word.save()


            
            # タグの更新処理
            tags_text = request.POST.get("tags", "")
            normalized_tags = unicodedata.normalize('NFKC', tags_text).replace('　', ' ')
            tag_names = normalized_tags.split()

            word.tags.clear() # 一旦リセット
            for name in tag_names:
                clean_name = name.lstrip('#＃')
                if clean_name:
                    tag, _ = Tag.objects.get_or_create(name=clean_name)
                    word.tags.add(tag)
                    

            messages.success(request, "更新しました")
            return redirect("words:word_list")
    else:
        form = WordForm(instance=word)

    # 編集画面の初期値として、既存のタグに # をつけて表示
    tags_str = " ".join([f"#{tag.name}" for tag in word.tags.all()])

    return render(
        request,
        "words/edit.html",
        {"form": form, "tags_str": tags_str, "word": word}
    )

def word_delete(request, word_id):
    # 自分の投稿だけを削除できるように取得
    word = get_object_or_404(Word, id=word_id, user=request.user)
    
    if request.method == "POST":
        word.delete()
        messages.info(request, "削除しました")
        # 削除が終わったら一覧画面へ戻る
        return redirect("words:word_list")
    
    # POST以外（URL直接入力など）で来たら、詳細画面に戻す
    return redirect("words:word_detail", word_id=word_id)