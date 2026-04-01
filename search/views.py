import unicodedata
from django.shortcuts import render
from django.db.models import Q
from words.models import Word
import random
from django.core.paginator import Paginator

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

    if raw_query:
        normalized_query = unicodedata.normalize('NFKC', raw_query).replace('　', ' ')
        decomposed_query = unicodedata.normalize('NFD', normalized_query)
        
        display_query = normalized_query
        
        clean_query = normalized_query.lstrip('#').strip()
        clean_decomposed = decomposed_query.lstrip('#').strip()

        if clean_query or clean_decomposed: 

            words = Word.objects.filter(

                Q(tags__name__icontains=clean_query) |      
                Q(tags__name__icontains=clean_decomposed) | 

                Q(content__icontains=clean_query) |         
                Q(content__icontains=clean_decomposed) |    

                Q(source_type__icontains=clean_query) |    
                Q(source_type__icontains=clean_decomposed) |

                Q(source_title__icontains=clean_query) |   
                Q(source_title__icontains=clean_decomposed) |

                Q(source_creator__icontains=clean_query) | 
                Q(source_creator__icontains=clean_decomposed)
            ).distinct()

            words = words.filter(is_public=True).order_by("-created_at")

    paginator = Paginator(words, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search/results.html', {
        'page_obj': page_obj,
        'query': display_query
    })

