from django.urls import path
app_name = 'content'
from .views import (
    HomeView, DepartmentsView, PageDetailView, DepartmentDetailView, 
    ProgramDetailView, NewsListView, NewsDetailView, GalleryView, 
    GalleryDetailView, NoticeListView, NoticeDetailView, ContactView,
    ProgramsListView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('departments/', DepartmentsView.as_view(), name='departments'),
    path('programs/', ProgramsListView.as_view(), name='programs_list'),
    path('departments/<slug:slug>/', DepartmentDetailView.as_view(), name='department_detail'),
    path('programs/<slug:slug>/', ProgramDetailView.as_view(), name='program_detail'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('gallery/', GalleryView.as_view(), name='gallery_list'),
    path('gallery/<slug:slug>/', GalleryDetailView.as_view(), name='gallery_detail'),
    path('notice/', NoticeListView.as_view(), name='notice_list'),
    path('notice/<slug:slug>/', NoticeDetailView.as_view(), name='notice_detail'),
    path('contact-us/', ContactView.as_view(), name='contact_us'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
]