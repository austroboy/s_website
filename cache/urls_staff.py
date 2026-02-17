from django.urls import path
from .views import StaffListView, StaffDetailView

app_name = 'staff'

urlpatterns = [
    path('', StaffListView.as_view(), name='list'),
    path('<int:pk>/', StaffDetailView.as_view(), name='detail'),  
]