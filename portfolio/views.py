from django.shortcuts import render,redirect

def portfolio_view(request):
    return render(request, 'portfolio/portfolio.html')

# 検索画面に飛ばすビュー
def go_to_search(request):
    return redirect('search:index')  # searchアプリのindexビューにリダイレクト