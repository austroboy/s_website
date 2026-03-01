from django.urls import path
from .views import ProgramListView, ProgramDetailView

app_name = 'programs'

urlpatterns = [
    path('', ProgramListView.as_view(), name='list'),
    path('<int:pk>/', ProgramDetailView.as_view(), name='detail'),
]