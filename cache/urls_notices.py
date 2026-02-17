from django.urls import path
from .views import NoticeListView, NoticeDetailView

app_name = 'notices'

urlpatterns = [
    path('', NoticeListView.as_view(), name='list'),
    path('<slug:slug>/', NoticeDetailView.as_view(), name='detail'),
]