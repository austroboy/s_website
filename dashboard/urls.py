# dashboard/urls.py
from django.urls import path
from . import views
from . import views_news
from . import views_events
from . import views_notices
from . import views_staff
from . import views_albums
from . import views_programs  # Add this import


urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path("login/", views.login_view, name="login"),
    
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
    
    # Notice management
    path('notices/', views_notices.dashboard_notice_list, name='notice_list'),
    path('notices/create/', views_notices.dashboard_notice_create, name='notice_create'),
    path('notices/<int:notice_id>/edit/', views_notices.dashboard_notice_edit, name='notice_edit'),
    path('notices/<int:notice_id>/delete/', views_notices.dashboard_notice_delete, name='notice_delete'),
    path('notices/<int:notice_id>/preview/', views_notices.dashboard_notice_preview, name='notice_preview'),
    path('notices/bulk-action/', views_notices.dashboard_notice_bulk_action, name='notice_bulk_action'),
    
    # Staff management
    path('staff/', views_staff.dashboard_staff_list, name='staff_list'),
    path('staff/create/', views_staff.dashboard_staff_create, name='staff_create'),
    path('staff/<int:staff_id>/edit/', views_staff.dashboard_staff_edit, name='staff_edit'),
    path('staff/<int:staff_id>/delete/', views_staff.dashboard_staff_delete, name='staff_delete'),
    path('staff/bulk-action/', views_staff.dashboard_staff_bulk_action, name='staff_bulk_action'),
    path('staff/reorder/', views_staff.dashboard_staff_reorder, name='staff_reorder'),
    
    # Album/Gallery management
    path('albums/', views_albums.dashboard_album_list, name='album_list'),
    path('albums/create/', views_albums.dashboard_album_create, name='album_create'),
    path('albums/<int:album_id>/edit/', views_albums.dashboard_album_edit, name='album_edit'),
    path('albums/<int:album_id>/delete/', views_albums.dashboard_album_delete, name='album_delete'),
    path('albums/<int:album_id>/preview/', views_albums.dashboard_album_preview, name='album_preview'),
    path('albums/bulk-action/', views_albums.dashboard_album_bulk_action, name='album_bulk_action'),
    path('albums/upload-media/', views_albums.dashboard_album_upload_media, name='album_upload_media'),
    
    # Program management
    path('programs/', views_programs.dashboard_program_list, name='program_list'),
    path('programs/create/', views_programs.dashboard_program_create, name='program_create'),
    path('programs/<int:program_id>/edit/', views_programs.dashboard_program_edit, name='program_edit'),
    path('programs/<int:program_id>/delete/', views_programs.dashboard_program_delete, name='program_delete'),
    path('programs/bulk-action/', views_programs.dashboard_program_bulk_action, name='program_bulk_action'),
    path('programs/reorder/', views_programs.dashboard_program_reorder, name='program_reorder'),
]