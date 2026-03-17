from django.shortcuts import render
from django.db.models import Q
from words.models import Word   

# Create your views here.
#検索ページ
def index(request):
    return render(request, "search/index.html")


#検索結果ページ
def results(request):
    query = request.GET.get('q', '').strip()
    words = Word.objects.none()

    if query:
        if '#' in query:
            # タグ検索
            words = Word.objects.filter(tags__icontains=query)
        else:
            # キーワード検索（本文 OR 出典）
            words = Word.objects.filter(
                Q(content__icontains=query) | Q(source_type__icontains=query)
            )

    return render(request, 'search/index.html', {'words': words, 'query': query})
