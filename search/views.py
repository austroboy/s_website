from django.views.generic import ListView
from django.db.models import Q
from cache.models import CachedNews, CachedEvent, CachedNotice, CachedStaff, CachedProgram
from content.models import Page

class SearchResultsView(ListView):
    template_name = 'search/results.html'
    context_object_name = 'results'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return []

        tenant = self.request.tenant
        results = []

        # Search news
        news_qs = CachedNews.objects.filter(
            tenant=tenant, is_published=True
        ).filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(summary__icontains=query)
        )[:10]
        for item in news_qs:
            results.append({'type': 'News', 'title': item.title, 'url': item.get_absolute_url(), 'date': item.created_at})

        # Search events
        event_qs = CachedEvent.objects.filter(
            tenant=tenant, is_published=True
        ).filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(summary__icontains=query)
        )[:10]
        for item in event_qs:
            results.append({'type': 'Event', 'title': item.title, 'url': item.get_absolute_url(), 'date': item.start_date})

        # Search notices
        notice_qs = CachedNotice.objects.filter(
            tenant=tenant, is_published=True
        ).filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(summary__icontains=query)
        )[:10]
        for item in notice_qs:
            results.append({'type': 'Notice', 'title': item.title, 'url': item.get_absolute_url(), 'date': item.created_at})

        # Search staff
        staff_qs = CachedStaff.objects.filter(
            tenant=tenant, is_published=True
        ).filter(
            Q(name__icontains=query) | Q(designation__icontains=query) | Q(bio__icontains=query)
        )[:10]
        for item in staff_qs:
            results.append({'type': 'Staff', 'title': item.name, 'url': item.get_absolute_url(), 'date': None})

        # Search programs
        prog_qs = CachedProgram.objects.filter(
            tenant=tenant, is_published=True
        ).filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )[:10]
        for item in prog_qs:
            results.append({'type': 'Program', 'title': item.name, 'url': item.get_absolute_url(), 'date': None})

        # Search pages
        page_qs = Page.objects.filter(
            tenant=tenant, published=True
        ).filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(meta_description__icontains=query)
        )[:10]
        for item in page_qs:
            results.append({'type': 'Page', 'title': item.title, 'url': item.get_absolute_url(), 'date': None})

        # Sort by relevance? For simplicity, we'll return combined list.
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context