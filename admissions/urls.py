from django.urls import path
from .views import AdmissionsOverviewView, AdmissionThankYouView

app_name = 'admissions'

urlpatterns = [
    path('', AdmissionsOverviewView.as_view(), name='overview'),
    path('thank-you/', AdmissionThankYouView.as_view(), name='thank_you'),
]