from django.views.generic import DetailView
from .models import Page

class PageDetailView(DetailView):
    model = Page
    template_name = 'content/page_detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        # Only pages belonging to current tenant and published
        return super().get_queryset().filter(tenant=self.request.tenant, published=True)
    
from django.views.generic import DetailView, TemplateView
from .models import Page, HomepageSection
from cache.models import CachedNews, CachedEvent, CachedNotice, CachedProgram, CachedAlbum
from django.utils.timezone import now
from django.db.models import Q

class HomeView(TemplateView):
    template_name = 'content/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = self.request.tenant

        # Homepage sections (configured in admin)
        sections = HomepageSection.objects.filter(tenant=tenant, is_active=True).order_by('order')
        context['sections'] = sections

        # Additional data for direct use in template (fallback if sections not used)
        context['programs'] = CachedProgram.objects.filter(tenant=tenant, is_published=True).order_by('order')[:4]
        context['news_list'] = CachedNews.objects.filter(tenant=tenant, is_published=True).order_by('-created_at')[:3]
        context['events_list'] = CachedEvent.objects.filter(
            tenant=tenant, is_published=True, start_date__gte=now()
        ).order_by('start_date')[:3]
        context['notices_list'] = (
            CachedNotice.objects.filter(tenant=tenant, is_published=True)
            .filter(Q(expiry_date__gte=now()) | Q(expiry_date__isnull=True))
            .order_by('-created_at')[:5]
        )
        # If you have a Testimonial model, add it here
        context['gallery_albums'] = CachedAlbum.objects.filter(tenant=tenant, is_published=True)[:4]

        # Hero section (optional – you can create a HomepageHero model or use section)
        context['hero'] = {
            'title': sections.filter(section_type='hero').first().title if sections.filter(section_type='hero').exists() else None,
            'subtitle': sections.filter(section_type='hero').first().subtitle if sections.filter(section_type='hero').exists() else None,
            # Add more fields as needed
        }
        return context

class PageDetailView(DetailView):
    model = Page
    template_name = 'content/page_detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        return super().get_queryset().filter(tenant=self.request.tenant, published=True)