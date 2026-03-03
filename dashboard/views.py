"""
views/dashboard.py — Dashboard homepage view + navigation context builder
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from cache.models import (
    CachedNews, CachedEvent, CachedNotice,
    CachedProgram, CachedStaff
)
from contact.models import AdmissionInquiry
from content.models import HomepageSection


# ──────────────────────────────────────────────────────────
#  Navigation structure — drives the right-sidebar menu
#  Each item is a dict:
#    { label, url, icon, badge (optional), active (set in view),
#      children: [ { label, url, badge, active } ] }
# ──────────────────────────────────────────────────────────

def build_nav_context(request):
    """Build the three navigation sections for the sidebar."""

    path = request.path

    def is_active(url):
        return path == url or path.startswith(url.rstrip('/') + '/')

    nav_main = [
        {
            'label': 'Overview',
            'url':   '/dashboard/',
            'icon':  'layout-dashboard',
            'active': is_active('/dashboard/'),
        },
        {
            'label': 'Admissions',
            'url':   '#',
            'icon':  'clipboard-list',
            'active': is_active('/admissions/'),
            'children': [
                {'label': 'Inquiries',     'url': '/admissions/inquiries/',    'active': is_active('/admissions/inquiries/')},
                {'label': 'Forms',         'url': '/admissions/forms/',        'active': is_active('/admissions/forms/')},
                {'label': 'Applications',  'url': '/admissions/applications/', 'active': is_active('/admissions/applications/')},
            ],
        },
        {
            'label': 'Academics',
            'url':   '#',
            'icon':  'graduation-cap',
            'active': is_active('/academics/'),
            'children': [
                {'label': 'Programs',    'url': '/academics/programs/',    'active': is_active('/academics/programs/')},
                {'label': 'Departments', 'url': '/academics/departments/', 'active': is_active('/academics/departments/')},
                {'label': 'Curriculum',  'url': '/academics/curriculum/',  'active': is_active('/academics/curriculum/')},
            ],
        },
        {
            'label': 'Staff Directory',
            'url':   '/staff/',
            'icon':  'contact',
            'active': is_active('/staff/'),
        },
    ]

    nav_content = [
        {
            'label': 'News & Stories',
            'url':   '#',
            'icon':  'newspaper',
            'active': is_active('/news/'),
            'children': [
                {'label': 'All Articles',  'url': '/news/',             'active': path == '/news/'},
                {'label': 'Create Article','url': '/news/create/',      'active': is_active('/news/create/')},
                {'label': 'Categories',    'url': '/news/categories/',  'active': is_active('/news/categories/')},
            ],
        },
        {
            'label': 'Events',
            'url':   '/events/',
            'icon':  'calendar-days',
            'active': is_active('/events/'),
        },
        {
            'label': 'Notices',
            'url':   '/notices/',
            'icon':  'megaphone',
            'active': is_active('/notices/'),
            # Badge: count of active notices
            'badge': CachedNotice.objects.filter(
                tenant=request.tenant,
                is_published=True,
                expiry_date__gte=timezone.now()
            ).count() or None,
        },
        {
            'label': 'Gallery',
            'url':   '#',
            'icon':  'image',
            'active': is_active('/gallery/'),
            'children': [
                {'label': 'Albums',      'url': '/gallery/albums/',  'active': is_active('/gallery/albums/')},
                {'label': 'Upload Media','url': '/gallery/upload/',  'active': is_active('/gallery/upload/')},
            ],
        },
        {
            'label': 'Achievements',
            'url':   '/achievements/dashboard/achievements/',
            'icon':  'trophy',
            'active': is_active('/achievements/dashboard/achievements/'),
        },
    ]

    nav_system = [
        {
            'label': 'Branding',
            'url':   '#',
            'icon':  'palette',
            'active': is_active('/settings/branding/'),
            'children': [
                {'label': 'Colors', 'url': '/dashboard/settings/branding/colors/', 'active': is_active('/settings/branding/colors/')},
                {'label': 'Fonts', 'url': '/dashboard/fonts', 'active': is_active('/fonts')},
                {'label': 'Logo & Assets',  'url': '/dashboard/settings/branding/assets/', 'active': is_active('/settings/branding/assets/')},
            ],
        },
        {
            'label': 'Navigation',
            'url':   '/settings/navigation/',
            'icon':  'menu',
            'active': is_active('/settings/navigation/'),
        },
        {
            'label': 'Homepage Builder',
            'url':   '/settings/homepage/', 
            'icon':  'layout-template',
            'active': is_active('/settings/homepage/'),
        },
        {
            'label': 'SMS Integration',
            'url':   '/settings/sms/',
            'icon':  'plug-2',
            'active': is_active('/settings/sms/'),
        },
        {
            'label': 'Contact & Forms',
            'url':   '/contact/submissions/',
            'icon':  'mail',
            'active': is_active('/contact/'),
        },
    ]

    return {
        'nav_main':    nav_main,
        'nav_content': nav_content,
        'nav_system':  nav_system,
    }


# ──────────────────────────────────────────────────────────
#  Dashboard Home View
# ──────────────────────────────────────────────────────────

@login_required
def dashboard_home(request):
    tenant = request.tenant  # set by TenantMiddleware
    print(request.user)
    print(request.user.is_authenticated)

    # ── Content Queries ────────────────────────────────────
    recent_news = CachedNews.objects.filter(
        tenant=tenant, is_published=True
    ).order_by('-created_at')[:5]

    upcoming_events = CachedEvent.objects.filter(
        tenant=tenant,
        is_published=True,
        start_date__gte=timezone.now()
    ).order_by('start_date')[:6]

    active_notices = CachedNotice.objects.filter(
        tenant=tenant,
        is_published=True,
        expiry_date__gte=timezone.now()
    ).order_by('-created_at')[:6]

    programs = CachedProgram.objects.filter(
        tenant=tenant, is_published=True
    ).order_by('order')[:8]

    staff_members = CachedStaff.objects.filter(
        tenant=tenant, is_published=True
    ).order_by('order')[:6]

    recent_inquiries = AdmissionInquiry.objects.filter(
        tenant=tenant
    ).order_by('-created_at')[:6]

    # ── KPI Stats ──────────────────────────────────────────
    homepage_stats = HomepageSection.objects.filter(
        tenant=tenant, section_type='stats'
    ).first()
    stats = homepage_stats.config if homepage_stats else {}

    # ── Counts for badges ──────────────────────────────────
    notices_count  = active_notices.count()
    inquiries_count = AdmissionInquiry.objects.filter(tenant=tenant).count()

    context = {
        'tenant':            tenant,
        'recent_news':       recent_news,
        'upcoming_events':   upcoming_events,
        'active_notices':    active_notices,
        'programs':          programs,
        'staff_members':     staff_members,
        'recent_inquiries':  recent_inquiries,
        'stats':             stats,
        'notices_count':     notices_count,
        'inquiries_count':   inquiries_count,
        **build_nav_context(request),
    }

    return render(request, 'dashboard/home.html', context)