from django.urls import include, path

urlpatterns = [
    # path('news/', include('cache.urls_news')),
    path('events/', include('cache.urls_events')),
    path('notices/', include('cache.urls_notices')),
    path('staff/', include('cache.urls_staff')),
    path('academics/', include('cache.urls_programs')),
    # path('gallery/', include('cache.urls_albums')),
    path('contact/', include('contact.urls')),
    path('admissions/', include('admissions.urls')),
    path('achievements/', include('achievements.urls')),
    path('documents/', include('documents.urls')),
    path('search/', include('search.urls')),

    path('', include('content.urls')),
]