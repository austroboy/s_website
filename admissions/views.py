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
    template_name = 'admissions/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = AdmissionForm.objects.filter(
            tenant=self.request.tenant, is_published=True
        ).order_by('order')
        context['inquiry_form'] = AdmissionInquiryForm()
        return context

    def post(self, request, *args, **kwargs):
        form = AdmissionInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.tenant = request.tenant
            inquiry.save()
            return redirect('admissions:thank_you')
        # if invalid, re-render with errors
        context = self.get_context_data()
        context['inquiry_form'] = form
        return self.render_to_response(context)

class AdmissionThankYouView(TemplateView):
    template_name = 'admissions/thank_you.html'