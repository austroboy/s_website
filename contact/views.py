from django.views.generic import FormView, CreateView
from django.urls import reverse_lazy
from .models import ContactSubmission, AdmissionInquiry
from .forms import ContactForm, AdmissionInquiryForm
from django.views.generic import TemplateView

class ContactFormView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact-success')

    def form_valid(self, form):
        # Save with tenant
        submission = form.save(commit=False)
        submission.tenant = self.request.tenant
        submission.ip_address = self.request.META.get('REMOTE_ADDR')
        submission.save()
        # Optionally send email notification
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'contact/success.html'

class AdmissionInquiryCreateView(CreateView):
    model = AdmissionInquiry
    form_class = AdmissionInquiryForm
    template_name = 'contact/admission_inquiry.html'
    success_url = reverse_lazy('admission-thankyou')

    def form_valid(self, form):
        inquiry = form.save(commit=False)
        inquiry.tenant = self.request.tenant
        inquiry.save()
        return super().form_valid(form)