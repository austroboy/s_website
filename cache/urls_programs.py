from django.urls import path
from .views import ProgramListView

app_name = 'programs'

urlpatterns = [
    path('', ProgramListView.as_view(), name='list'),
]