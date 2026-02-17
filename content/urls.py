from django.urls import path
from .views import HomeView, PageDetailView

app_name = 'content'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page'),
]