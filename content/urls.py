from django.urls import path
app_name = 'content'
from .views import (
    HomeView, DepartmentsView, PageDetailView, DepartmentDetailView, 
    ProgramDetailView, NewsListView, NewsDetailView, GalleryView, 
    GalleryDetailView, NoticeListView, NoticeDetailView, ContactView,
    ProgramsListView
)
from .dashboard_views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('departments/', DepartmentsView.as_view(), name='departments'),
    path('programs/', ProgramsListView.as_view(), name='programs_list'),
    path('departments/<slug:slug>/', DepartmentDetailView.as_view(), name='department_detail'),
    path('programs/<slug:slug>/', ProgramDetailView.as_view(), name='program_detail'),
    # News and gallery are handled by cache apps now
    # path('gallery/', GalleryView.as_view(), name='gallery_list'),
    # path('gallery/<slug:slug>/', GalleryDetailView.as_view(), name='gallery_detail'),
    path('notice/', NoticeListView.as_view(), name='notice_list'),
    path('notice/<slug:slug>/', NoticeDetailView.as_view(), name='notice_detail'),
    path('contact-us/', ContactView.as_view(), name='contact_us'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
     path('settings/homepage/',                homepage_builder,         name='homepage_builder'),
    path('settings/homepage/<int:pk>/toggle/',homepage_section_toggle,  name='homepage_section_toggle'),
    path('settings/homepage/<int:pk>/delete/',homepage_section_delete,  name='homepage_section_delete'),
    path("settings/pages/", page_list, name="page_list"),
]