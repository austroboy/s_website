from django.views.generic import ListView
from .models import Document, DocumentCategory

class DocumentListView(ListView):
    model = Document
    template_name = 'documents/list.html'
    context_object_name = 'documents'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().filter(tenant=self.request.tenant, is_published=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DocumentCategory.objects.filter(tenant=self.request.tenant)
        context['current_category'] = None
        if 'category_slug' in self.kwargs:
            context['current_category'] = DocumentCategory.objects.filter(
                tenant=self.request.tenant, slug=self.kwargs['category_slug']
            ).first()
        return context