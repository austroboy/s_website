from django.urls import path
from .views import AlbumListView, AlbumDetailView

app_name = 'albums'

urlpatterns = [
    path('', AlbumListView.as_view(), name='list'),
    path('<slug:slug>/', AlbumDetailView.as_view(), name='detail'),
]