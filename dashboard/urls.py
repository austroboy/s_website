# dashboard/urls.py
from django.urls import path
from . import views
from . import views_news
from . import views_events


urlpatterns = [
    path('', views.dashboard_home, name='home'),
    
    # News management
    path('news/', views_news.dashboard_news_list, name='news_list'),
    path('news/create/', views_news.dashboard_news_create, name='news_create'),
    path('news/<int:news_id>/edit/', views_news.dashboard_news_edit, name='news_edit'),
    path('news/<int:news_id>/delete/', views_news.dashboard_news_delete, name='news_delete'),
    path('news/<int:news_id>/preview/', views_news.dashboard_news_preview, name='news_preview'),
    path('news/bulk-action/', views_news.dashboard_news_bulk_action, name='news_bulk_action'),
    
    # Event management
    path('events/', views_events.dashboard_event_list, name='event_list'),
    path('events/create/', views_events.dashboard_event_create, name='event_create'),
    path('events/<int:event_id>/edit/', views_events.dashboard_event_edit, name='event_edit'),
    path('events/<int:event_id>/delete/', views_events.dashboard_event_delete, name='event_delete'),
    path('events/<int:event_id>/preview/', views_events.dashboard_event_preview, name='event_preview'),
    path('events/bulk-action/', views_events.dashboard_event_bulk_action, name='event_bulk_action'),
]