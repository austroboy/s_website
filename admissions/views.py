from django.views.generic import TemplateView, ListView
from .models import AdmissionForm
from contact.forms import AdmissionInquiryForm

class AdmissionsOverviewView(TemplateView):
    template_name = 'admissions/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = AdmissionForm.objects.filter(
            tenant=self.request.tenant, is_published=True
        ).order_by('order')
        context['inquiry_form'] = AdmissionInquiryForm()
        return context

# You may also want a separate inquiry page, but we already have /contact/admissions/.
# To keep consistent, we'll include the inquiry form on the overview page and handle POST there.
from django.urls import reverse_lazy
from django.shortcuts import redirect
from contact.models import AdmissionInquiry

class AdmissionsOverviewView(TemplateView):
    template_name = 'components/page/details/admissions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all published admission forms for the current tenant
        context['forms'] = AdmissionForm.objects.filter(
            tenant=self.request.tenant, is_published=True
        ).order_by('order')
        
        # Add the inquiry form for the sidebar/bottom section
        context['inquiry_form'] = AdmissionInquiryForm()
        
        return context
        return context

class AdmissionThankYouView(TemplateView):
    template_name = 'admissions/thank_you.html'