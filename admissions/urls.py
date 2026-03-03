from django.urls import path
from .views import AdmissionsOverviewView, AdmissionDetailView, AdmissionThankYouView

app_name = 'admissions'

urlpatterns = [
    path('', AdmissionsOverviewView.as_view(), name='overview'),
    path('thank-you/', AdmissionThankYouView.as_view(), name='thank_you'),
    path('<int:pk>/', AdmissionDetailView.as_view(), name='detail'),
]
