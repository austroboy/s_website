# cache/urls_news.py
from django.urls import path
from .views import NewsListView, NewsDetailView

urlpatterns = [
    path('', NewsListView.as_view(), name='news-list'),
    path('<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
]