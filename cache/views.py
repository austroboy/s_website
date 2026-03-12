# cache/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from tenants.models import Tenant
from .models import CachedNews, CachedEvent, CachedNotice
from django.db.models import Q
from django.utils.timezone import now

class WebhookNewsUpdate(APIView):
    def post(self, request):
        # হেডার থেকে টেনেন্ট আইডি নাও
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return Response({'error': 'Missing X-Tenant-ID header'}, status=status.HTTP_400_BAD_REQUEST)
        
        tenant = get_object_or_404(Tenant, sms_tenant_id=tenant_id)
        action = request.data.get('action')  # 'create', 'update', 'delete'
        sms_id = request.data.get('id')
        data = request.data.get('data', {})  # পূর্ণ ডেটা পেলেও আসতে পারে

        if action == 'delete':
            CachedNews.objects.filter(tenant=tenant, sms_id=sms_id).delete()
            return Response({'status': 'deleted'}, status=status.HTTP_200_OK)

        # action create বা update
        # যদি data না দেয়া হয়, তাহলে আমরা নিজেরাই এসএমএস থেকে fetch করতে পারি
        if not data:
            # ফেচ করার লজিক (নিচের টাস্ক ব্যবহার করতে পারে)
            pass
        else:
            # ডেটা ম্যাপ করে সেভ করো
            CachedNews.objects.update_or_create(
                tenant=tenant,
                sms_id=sms_id,
                defaults={
                    'title': data.get('title', ''),
                    'content': data.get('content', ''),
                    'summary': data.get('summary', ''),
                    'featured_image': data.get('featured_image', ''),
                    'created_at': data.get('created_at'),
                    'updated_at': data.get('updated_at'),
                    'author_name': data.get('author_name', ''),
                    # ... বাকি ফিল্ড
                }
            )
        return Response({'status': 'updated'}, status=status.HTTP_200_OK)
    
    
    
from django.views.generic import ListView, DetailView
from .models import (
    CachedNews, CachedEvent, CachedNotice,
    CachedStaff, CachedProgram, CachedAlbum
)

# ---- News ----
class NewsListView(ListView):
    model = CachedNews
    template_name = 'components/page/list/news.html'
    context_object_name = 'news_list'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from content.models import HomepageSection
        context['section'] = HomepageSection.objects.filter(
            tenant=self.request.tenant, section_type='news', is_active=True
        ).first()
        return context


class NewsDetailView(DetailView):
    model = CachedNews
    template_name = 'components/page/details/news.html'
    context_object_name = 'news'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get 5 most popular/recent news for the sidebar (excluding current)
        context['popular_news'] = CachedNews.objects.filter(
            tenant=self.object.tenant, 
            is_published=True
        ).exclude(id=self.object.id).order_by('-created_at')[:5]
        return context

# ---- Events ----
class EventListView(ListView):
    model = CachedEvent
    template_name = 'components/page/list/event.html'
    context_object_name = 'events'
    paginate_by = 6

    def get_queryset(self):
        # Upcoming events first
        return super().get_queryset().filter(is_published=True).order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from content.models import HomepageSection
        context['section'] = HomepageSection.objects.filter(
            tenant=self.request.tenant, section_type='events', is_active=True
        ).first()
        return context

class EventDetailView(DetailView):
    model = CachedEvent
    template_name = 'components/page/details/event.html'
    context_object_name = 'event'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

# ---- Notices ----
class NoticeListView(ListView):
    model = CachedNotice
    template_name = 'components/page/list/notice.html'
    context_object_name = 'notices_list'
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset().filter(is_published=True)
        qs = qs.filter(Q(expiry_date__gte=now()) | Q(expiry_date__isnull=True))
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from content.models import HomepageSection
        context['section'] = HomepageSection.objects.filter(
            tenant=self.request.tenant, section_type='notices', is_active=True
        ).first()
        return context

class NoticeDetailView(DetailView):
    model = CachedNotice
    template_name = 'components/page/details/notice.html'
    context_object_name = 'notice'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

# ---- Staff Directory ----
class StaffListView(ListView):
    model = CachedStaff
    template_name = 'components/page/list/staff.html'
    context_object_name = 'staff_list'
    paginate_by = 6

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).order_by('order', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from content.models import HomepageSection
        context['section'] = HomepageSection.objects.filter(
            tenant=self.request.tenant, section_type='staff', is_active=True
        ).first()
        return context

class StaffDetailView(DetailView):
    model = CachedStaff
    template_name = 'components/page/details/staff.html'
    context_object_name = 'staff'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get 5-6 other staff members from the same tenant for the sidebar
        context['other_staff'] = CachedStaff.objects.filter(
            tenant=self.object.tenant, 
            is_published=True
        ).exclude(id=self.object.id).order_by('?')[:6]
        return context

# ---- Programs (Academics) ----
class ProgramListView(ListView):
    model = CachedProgram
    template_name = 'components/page/list/programs.html'
    context_object_name = 'programs'
    paginate_by = 6

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from content.models import HomepageSection
        context['section'] = HomepageSection.objects.filter(
            tenant=self.request.tenant, section_type='features', is_active=True
        ).first()
        return context

class ProgramDetailView(DetailView):
    model = CachedProgram
    template_name = 'components/page/details/programs.html'
    context_object_name = 'program'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

# ---- Gallery ----
class AlbumListView(ListView):
    model = CachedAlbum
    template_name = 'components/page/list/gallery.html'
    context_object_name = 'albums'
    paginate_by = 6

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from content.models import HomepageSection
        context['section'] = HomepageSection.objects.filter(
            tenant=self.request.tenant, section_type='gallery', is_active=True
        ).first()
        return context


class AlbumDetailView(DetailView):
    model = CachedAlbum
    template_name = 'components/page/details/gallery.html'
    context_object_name = 'album'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)