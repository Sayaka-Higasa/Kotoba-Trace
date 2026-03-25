from django.urls import path
from portfolio import views as portfolio_views

urlpatterns = [
    path("", portfolio_views.portfolio_view, name="portfolio"),  
]