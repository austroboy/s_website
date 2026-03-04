from django.urls import path
from .views import AdmissionsOverviewView, AdmissionThankYouView
from .import dashboard_views
from .views import AdmissionsOverviewView, AdmissionDetailView, AdmissionThankYouView

app_name = 'admissions'

urlpatterns = [
    path('', AdmissionsOverviewView.as_view(), name='overview'),
    path('thank-you/', AdmissionThankYouView.as_view(), name='thank_you'),
    #dashboard
    path("admission-forms/",
     dashboard_views.admission_form_list,
     name="admission_form_list"),

    path("admission-forms/<int:pk>/download/",
     dashboard_views.admission_form_download,
     name="admission_form_download"),
    path('<int:pk>/', AdmissionDetailView.as_view(), name='detail'),
]
