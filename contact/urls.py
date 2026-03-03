from django.urls import path
from .views import ContactFormView, ContactSuccessView, AdmissionInquiryCreateView
from .import dashboard_views
app_name = 'contact'

urlpatterns = [
    path('', ContactFormView.as_view(), name='contact'),
    path('success/', ContactSuccessView.as_view(), name='success'),
    path('admissions/', AdmissionInquiryCreateView.as_view(), name='admission'),
    #dashboard
    path(
    "admissions/inquiries/",
    dashboard_views.admission_inquiry_list,
    name="admission_inquiry_list",
),
path(
    "admission-inquiries/<int:pk>/toggle/",
    dashboard_views.admission_inquiry_toggle,
    name="admission_inquiry_toggle",
),
]