from django.urls import path
app_name = 'content'
from .views import (
    HomeView, PageDetailView
)
from .dashboard_views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
     path('settings/homepage/',                homepage_builder,         name='homepage_builder'),
    path('settings/homepage/<int:pk>/toggle/',homepage_section_toggle,  name='homepage_section_toggle'),
    path('settings/homepage/<int:pk>/delete/',homepage_section_delete,  name='homepage_section_delete'),
    path("settings/pages/", page_list, name="page_list"),
    path('settings/homepage/',homepage_builder,name='homepage_builder'),
    path('settings/homepage/<int:pk>/toggle/',homepage_section_toggle,name='homepage_section_toggle'),
    path('settings/homepage/<int:pk>/delete/',homepage_section_delete,name='homepage_section_delete'),
]