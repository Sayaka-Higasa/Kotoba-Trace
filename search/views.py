from django.shortcuts import render
from django.db.models import Q
from words.models import Word
import random

# 検索ページ（検索窓 + ランダムカード2件表示）
def index(request):
    # 公開されている言葉を取得
    candidates = Word.objects.filter(is_public=True).order_by('-id')

    # 自分の投稿は除外
    if request.user.is_authenticated:
        candidates = candidates.exclude(user=request.user)

    
    # 新着10件からランダム2件
    candidates = candidates[:10]
    random_words = random.sample(list(candidates), min(2, len(candidates)))

    return render(request, "search/index.html", {"random_words": random_words})


# 検索結果ページ
def results(request):
    query = request.GET.get('q', '').strip()
    words = Word.objects.none()

    if query:
        if query.startswith('#'):
            # タグ検索
            tag_keyword = query.lstrip("#")
            words = Word.objects.filter(
                tags__name__icontains=tag_keyword
            ).distinct()
        else:
            # キーワード検索（本文 OR 出典）
            words = Word.objects.filter(
                Q(content__icontains=query) | 
                Q(source_type__icontains=query) |
                Q(source_title__icontains=query) |
                Q(source_creator__icontains=query)
            ).distinct()
        words = words.order_by("-created_at")

        if request.user.is_authenticated:
            words = words.exclude(user=request.user)

    return render(request, 'search/results.html', {'words': words, 'query': query})