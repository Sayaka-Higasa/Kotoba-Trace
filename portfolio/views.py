from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def portfolio_view(request):
    return render(request, 'portfolio/portfolio.html')