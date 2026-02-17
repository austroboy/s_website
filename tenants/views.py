from django.urls import include, path

urlpatterns = [
    path('', include('content.urls')),
    path('news/', include('cache.urls_news')),
    path('events/', include('cache.urls_events')),
    path('notices/', include('cache.urls_notices')),
    path('staff/', include('cache.urls_staff')),
    path('academics/', include('cache.urls_programs')),
    path('gallery/', include('cache.urls_albums')),
    path('contact/', include('contact.urls')),
]