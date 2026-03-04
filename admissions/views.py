from django.views.generic import ListView, DetailView, TemplateView
from .models import AdmissionForm
from contact.forms import AdmissionInquiryForm

class AdmissionsOverviewView(ListView):
    model = AdmissionForm
    template_name = 'components/page/list/admissions_form.html'
    context_object_name = 'forms'
    paginate_by = 12

    def get_queryset(self):
        return AdmissionForm.objects.filter(
            tenant=self.request.tenant, is_published=True
        ).order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inquiry_form'] = AdmissionInquiryForm()
        return context

class AdmissionDetailView(DetailView):
    model = AdmissionForm
    template_name = 'components/page/details/admissions.html'
    context_object_name = 'form'

    def get_queryset(self):
        return AdmissionForm.objects.filter(
            tenant=self.request.tenant, is_published=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inquiry_form'] = AdmissionInquiryForm()
        # Fetch other forms (excluding current one)
        context['other_forms'] = AdmissionForm.objects.filter(
            tenant=self.request.tenant, 
            is_published=True
        ).exclude(pk=self.object.pk).order_by('order')[:5]
        return context

class AdmissionThankYouView(TemplateView):
    template_name = 'components/page/details/thank_you.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inquiry_form'] = AdmissionInquiryForm()
        return context