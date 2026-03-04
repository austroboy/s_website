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
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages




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
                {'label': 'Inquiries',     'url': '/contact/admissions/inquiries/',    'active': is_active('/dashboard/admissions/inquiries/')},
                {'label': 'Forms',         'url': '/admissions/admission-forms/',        'active': is_active('/admissions/admission-forms/')},
                {'label': 'Applications',  'url': '/admissions/applications/', 'active': is_active('/admissions/applications/')},
            ],
        },
        # Academics section
        {
            'label': 'Academics',
            'url':   '#',
            'icon':  'graduation-cap',
            'active': is_active('/dashboard/programs/'),
            'children': [
                {'label': 'Programs',    'url': '/dashboard/programs/',    'active': is_active('/dashboard/programs/')},
                # {'label': 'Departments', 'url': '/academics/departments/', 'active': is_active('/academics/departments/')},
                # {'label': 'Curriculum',  'url': '/academics/curriculum/',  'active': is_active('/academics/curriculum/')},
            ],
        },
        {
            'label': 'Staff Directory',
            'url':   '/dashboard/staff/',  
            'icon':  'contact',
            'active': is_active('/dashboard/staff/'),
        },
    ]

    nav_content = [
        {
        'label': 'News & Stories',
        'url':   '#',
        'icon':  'newspaper',
        'active': is_active('/dashboard/news/'),
        'children': [
            {'label': 'All News',  'url': '/dashboard/news/', 'active': is_active('/dashboard/news/')},
            {'label': 'Create Article', 'url': '/dashboard/news/create/', 'active': is_active('/dashboard/news/create/')},
            # {'label': 'Categories', 'url': '/news/categories/', 'active': is_active('/news/categories/')},
        ],
        },
        {
        'label': 'Documents',
        'url':   '#',
        'icon':  'file-text',
        'active': is_active('/documents/'),
        'children': [
            {'label': 'Documents Category',  'url': '/documents/dashboard/category/', 'active': is_active('/documents/dashboard/category/')},
            {'label': 'Documents',  'url': '/documents/dashboard/documents/', 'active': is_active('/documents/dashboard/documents/')},
        ],
        },
        {
            'label': 'Events',
            'url':   '#',
            'icon':  'calendar-days',
            'active': is_active('/dashboard/events/') or is_active('/events/'),
            'children': [
                {
                    'label': 'All Events',  
                    'url': '/dashboard/events/', 
                    'active': is_active('/dashboard/events/'),
                },
                {
                    'label': 'Create Event', 
                    'url': '/dashboard/events/create/', 
                    'active': is_active('/dashboard/events/create/')
                },
                # {
                #     'label': 'Calendar View', 
                #     'url': '/events/calendar/', 
                #     'active': is_active('/events/calendar/')
                # },
            ],
        },
        {
            'label': 'Notices',
            'url':   '#',
            'icon':  'megaphone',
            'active': is_active('/dashboard/notices/'),
            'children': [
                {'label': 'All Notices',    'url': '/dashboard/notices/',        'active': is_active('/dashboard/notices/')},
                {'label': 'Create Notice',  'url': '/dashboard/notices/create/', 'active': is_active('/dashboard/notices/create/')},
            ],
            # Badge: count of active notices
            'badge': CachedNotice.objects.filter(
                tenant=request.tenant,
                is_published=True,
                expiry_date__gte=timezone.now().date()
            ).count() or None,
        },
        # In dashboard/views.py, update the Gallery entry in nav_content
        {
            'label': 'Gallery',
            'url':   '#',
            'icon':  'image',
            'active': is_active('/dashboard/albums/') or is_active('/gallery/'),
            'children': [
                {'label': 'All Albums',      'url': '/dashboard/albums/',  'active': is_active('/dashboard/albums/')},
                {'label': 'Create Album',    'url': '/dashboard/albums/create/',  'active': is_active('/dashboard/albums/create/')},
                # {'label': 'Upload Media',    'url': '/dashboard/albums/create/#upload',  'active': False},
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
            'url':   '/navigation/menus/',
            'icon':  'menu',
            'active': is_active('/navigation/'),
        },
        {
            'label': 'Homepage Builder',
            'url':   '/settings/homepage/', 
            'icon':  'layout-template',
            'active': is_active('/settings/homepage/'),
        },
        {
            'label': 'Pages',
            'url':   '/settings/pages/', 
            'icon':  'book',
            'active': is_active('/settings/pages/'),
        },
        {
            'label': 'SMS Integration',
            'url':   '/settings/sms/',
            'icon':  'plug-2',
            'active': is_active('/settings/sms/'),
        },
        {
            'label': 'Contact & Forms',
            'url':   '/contact/contact-submissions/',
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


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')  # or 'login' or any other page




def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")  # change to your dashboard url name

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # change if needed
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "dashboard/auth/login.html")