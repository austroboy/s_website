from django.urls import path
from .views import AchievementListView, AchievementDetailView

app_name = 'achievements'

urlpatterns = [
    path('', AchievementListView.as_view(), name='list'),
    path('<int:pk>/', AchievementDetailView.as_view(), name='detail'),
]