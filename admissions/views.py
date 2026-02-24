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
        
        # New Structured Content for Sidebar Layout
        context['admissions'] = {
            'title': 'Undergraduate and Graduate Admissions',
            'sections': [
                {
                    'id': 'requirements',
                    'title': 'Admission Requirements',
                    'contentHtml': '''
                        <div class="space-y-4">
                            <h4 class="font-bold text-[var(--secondary)]">Undergraduate Programs</h4>
                            <p>Minimum GPA of 2.50 in both SSC and HSC examinations. For O-Level, 5 subjects must be passed and for A-Level, 2 subjects must be passed with a minimum grade of C.</p>
                            <h4 class="font-bold text-[var(--secondary)] mt-6">Graduate Programs</h4>
                            <p>Successful completion of an Undergraduate degree from a recognized university with a minimum CGPA of 2.50 or equivalent.</p>
                        </div>
                    '''
                },
                {
                    'id': 'procedure',
                    'title': 'Admission Procedure',
                    'contentHtml': '''
                        <ol class="list-decimal pl-5 space-y-3">
                            <li>Create an account on the online admission portal.</li>
                            <li>Fill out the application form with personal and academic details.</li>
                            <li>Upload required documents (Photo, Certificates, Transcripts).</li>
                            <li>Pay the application fee via the integrated payment gateway.</li>
                            <li>Download the admit card for the admission test.</li>
                        </ol>
                    '''
                },
                {
                    'id': 'offering',
                    'title': 'Programs Offering',
                    'contentHtml': '''
                        <p class="mb-4">We offer a wide range of programs across our various schools:</p>
                        <ul class="list-disc pl-5 space-y-2">
                            <li><strong>School of Business & Economics:</strong> BBA, MBA, EMBA</li>
                            <li><strong>School of Engineering & Physical Sciences:</strong> CSE, EEE, Architecture</li>
                            <li><strong>School of Humanities & Social Sciences:</strong> English, Law, Economics</li>
                            <li><strong>School of Health & Life Sciences:</strong> Pharmacy, Microbiology</li>
                        </ul>
                    '''
                },
                {
                    'id': 'fees',
                    'title': 'Tuition Fees & Waiver',
                    'contentHtml': '''
                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200 text-sm">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th class="px-4 py-2 text-left font-bold text-[var(--secondary)]">Type</th>
                                        <th class="px-4 py-2 text-left font-bold text-[var(--secondary)]">Amount (BDT)</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-gray-200">
                                    <tr><td class="px-4 py-2">Admission Fee (One time)</td><td class="px-4 py-2">25,000/-</td></tr>
                                    <tr><td class="px-4 py-2">Tuition Fee (Per credit)</td><td class="px-4 py-2">6,500/-</td></tr>
                                    <tr><td class="px-4 py-2">Activity Fee (Per semester)</td><td class="px-4 py-2">3,000/-</td></tr>
                                </tbody>
                            </table>
                        </div>
                        <p class="mt-4 text-[var(--primary)] font-semibold">Scholarships up to 100% based on merit and financial need.</p>
                    '''
                },
                {
                    'id': 'enquiry',
                    'title': 'Admission Enquiry',
                    'contentHtml': 'render_form' # Placeholder to handle form rendering specially in template
                },
                {
                    'id': 'transfer',
                    'title': 'Credit Transfer Policy',
                    'contentHtml': '''
                        <p>Students from other recognized universities may apply for credit transfer. A minimum grade of 'B' is required for any course to be considered for transfer. A maximum of 50% of the total required credits for a program may be transferred.</p>
                    '''
                },
                {
                    'id': 'calendar',
                    'title': 'Academic Calendar',
                    'contentHtml': '''
                        <div class="space-y-4">
                            <div class="flex justify-between items-center p-4 bg-white border border-gray-100 rounded-xl shadow-sm">
                                <span>Admission Test (Phase 1)</span>
                                <span class="font-bold">April 15, 2026</span>
                            </div>
                            <div class="flex justify-between items-center p-4 bg-white border border-gray-100 rounded-xl shadow-sm">
                                <span>Orientation Program</span>
                                <span class="font-bold">May 10, 2026</span>
                            </div>
                            <div class="flex justify-between items-center p-4 bg-white border border-gray-100 rounded-xl shadow-sm">
                                <span>Classes Begin</span>
                                <span class="font-bold">May 15, 2026</span>
                            </div>
                        </div>
                    '''
                }
            ]
        }
        return context

class AdmissionThankYouView(TemplateView):
    template_name = 'admissions/thank_you.html'