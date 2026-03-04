from django.urls import path
from .views import DocumentListView
from . import dashboard_views

app_name = 'documents'

urlpatterns = [
    path('', DocumentListView.as_view(), name='list'),
    path('category/<slug:category_slug>/', DocumentListView.as_view(), name='category'),
    #dashboard
    path(
    "dashboard/category/",
    dashboard_views.document_category_list,
    name="document_category_list",
),
]