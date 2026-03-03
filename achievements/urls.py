from django.urls import path
from .views import AchievementListView, AchievementDetailView
from .import dashboard_views
app_name = 'achievements'

urlpatterns = [
    path('', AchievementListView.as_view(), name='list'),
    path('<int:pk>/', AchievementDetailView.as_view(), name='detail'),
    path(
        "dashboard/achievements/",
        dashboard_views.achievement_manager,
        name="achievement_manager",
    ),
    path(
        "dashboard/achievements/<int:pk>/delete/",
        dashboard_views.achievement_delete,
        name="achievement_delete",
    ),
]