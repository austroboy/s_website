from django.urls import path
from .views import DocumentListView

app_name = 'documents'

urlpatterns = [
    path('', DocumentListView.as_view(), name='list'),
    path('category/<slug:category_slug>/', DocumentListView.as_view(), name='category'),
]