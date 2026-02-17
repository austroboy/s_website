from django.urls import path
from .views import ContactFormView, ContactSuccessView, AdmissionInquiryCreateView

app_name = 'contact'

urlpatterns = [
    path('', ContactFormView.as_view(), name='contact'),
    path('success/', ContactSuccessView.as_view(), name='success'),
    path('admissions/', AdmissionInquiryCreateView.as_view(), name='admission'),
]