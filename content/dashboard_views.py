"""
views/homepage_builder.py — Homepage section CRUD views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import HomepageSection           # adjust import path
from dashboard.views import build_nav_context        # reuse sidebar nav


# ── Icon map for template filter (used in tag below) ──
SECTION_ICONS = {
    'hero':         'layout-panel-top',
    'features':     'graduation-cap',
    'stats':        'bar-chart-2',
    'news':         'newspaper',
    'events':       'calendar-days',
    'notices':      'megaphone',
    'testimonials': 'quote',
    'gallery':      'image',
    'achievements': 'trophy',
    'staff':        'contact',
    'cta':          'mouse-pointer-2',
}


def _build_config(post_data: dict, section_type: str) -> dict:
    """Extract typed config dict from POST data based on section_type."""
    cfg = {}
    if section_type == 'hero':
        cfg = {
            'cta_primary_text':   post_data.get('cfg_cta_primary_text', ''),
            'cta_primary_link':   post_data.get('cfg_cta_primary_link', ''),
            'cta_secondary_text': post_data.get('cfg_cta_secondary_text', ''),
            'cta_secondary_link': post_data.get('cfg_cta_secondary_link', ''),
            'background_image':   post_data.get('cfg_background_image', ''),
        }
    elif section_type == 'stats':
        def _int(key): 
            try: return int(post_data.get(key, 0) or 0)
            except (ValueError, TypeError): return 0
        cfg = {
            'students': _int('cfg_students'),
            'teachers': _int('cfg_teachers'),
            'programs': _int('cfg_programs'),
            'years':    _int('cfg_years'),
        }
    elif section_type == 'cta':
        cfg = {
            'primary_text':   post_data.get('cfg_primary_text', ''),
            'primary_link':   post_data.get('cfg_primary_link', ''),
            'secondary_text': post_data.get('cfg_secondary_text', ''),
            'secondary_link': post_data.get('cfg_secondary_link', ''),
        }
    # Sections without specific config just return {}
    return {k: v for k, v in cfg.items() if v or v == 0}


# ──────────────────────────────────────────────────────────
#  Main list + create/update view
# ──────────────────────────────────────────────────────────

@login_required
def homepage_builder(request):
    tenant   = request.tenant
    sections = HomepageSection.objects.filter(tenant=tenant)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            section_type = request.POST.get('section_type', '')
            section = HomepageSection(tenant=tenant)
            section.section_type = section_type
            section.title    = request.POST.get('title', '').strip()
            section.subtitle = request.POST.get('subtitle', '').strip()
            section.order    = int(request.POST.get('order') or 0)
            section.is_active = 'is_active' in request.POST
            section.config   = _build_config(request.POST, section_type)
            section.save()
            messages.success(request, 'Section created successfully.')
            return redirect('content:homepage_builder')

        elif action == 'update':
            section_id   = request.POST.get('section_id')
            section      = get_object_or_404(HomepageSection, id=section_id, tenant=tenant)
            section_type = request.POST.get('section_type', section.section_type)
            section.section_type = section_type
            section.title    = request.POST.get('title', '').strip()
            section.subtitle = request.POST.get('subtitle', '').strip()
            section.order    = int(request.POST.get('order') or 0)
            section.is_active = 'is_active' in request.POST
            section.config   = _build_config(request.POST, section_type)
            section.save()
            messages.success(request, 'Section updated successfully.')
            return redirect('content:homepage_builder')

    context = {
        'tenant':        tenant,
        'sections':      sections,
        'section_types': HomepageSection.SECTION_TYPES,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/home/homepage_builder.html', context)


# ──────────────────────────────────────────────────────────
#  Toggle active/inactive
# ──────────────────────────────────────────────────────────

@login_required
@require_POST
def homepage_section_toggle(request, pk):
    section = get_object_or_404(HomepageSection, id=pk, tenant=request.tenant)
    section.is_active = not section.is_active
    section.save(update_fields=['is_active'])
    status = 'activated' if section.is_active else 'deactivated'
    messages.success(request, f'Section {status}.')
    return redirect('content:homepage_builder')


# ──────────────────────────────────────────────────────────
#  Delete
# ──────────────────────────────────────────────────────────

@login_required
@require_POST
def homepage_section_delete(request, pk):
    section = get_object_or_404(HomepageSection, id=pk, tenant=request.tenant)
    section.delete()
    messages.success(request, 'Section deleted.')
    return redirect('content:homepage_builder')