import unicodedata
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
    raw_query = request.GET.get('q', '').strip()
    words = Word.objects.none()
    display_query = raw_query

    if  raw_query:
        normalized_query = unicodedata.normalize('NFKC', raw_query).replace('　', ' ')
        display_query = normalized_query
        clean_query = normalized_query.lstrip('#')
        words= Word.objects.filter(
            Q(tags__name__icontains=clean_query) |      
            Q(content__icontains=clean_query) |         
            Q(source_type__icontains=clean_query) |    
            Q(source_title__icontains=clean_query) |   
            Q(source_creator__icontains=clean_query)   
        ).distinct()

        #公開されてるものだけ
        words = words.filter(is_public=True).order_by("-created_at")

        #自分の投稿は表示されない
        # if request.user.is_authenticated:
        #     words = words.exclude(user=request.user)
    return render(request, 'search/results.html', {'words': words, 'query':  display_query})

