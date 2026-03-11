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
        bg_images = [
            post_data.get('cfg_bg_image_1', '').strip(),
            post_data.get('cfg_bg_image_2', '').strip(),
            post_data.get('cfg_bg_image_3', '').strip(),
            post_data.get('cfg_bg_image_4', '').strip(),
        ]
        cfg = {
            'cta_primary_text':   post_data.get('cfg_cta_primary_text', ''),
            'cta_primary_link':   post_data.get('cfg_cta_primary_link', ''),
            'cta_secondary_text': post_data.get('cfg_cta_secondary_text', ''),
            'cta_secondary_link': post_data.get('cfg_cta_secondary_link', ''),
            'background_images':  [img for img in bg_images if img],
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
            'bg_image': post_data.get('cfg_stats_bg_image', '').strip(),
        }
    elif section_type == 'cta':
        cfg = {
            'cta_primary_text':   post_data.get('cfg_primary_text', ''),
            'cta_primary_link':   post_data.get('cfg_primary_link', ''),
            'cta_secondary_text': post_data.get('cfg_secondary_text', ''),
            'cta_secondary_link': post_data.get('cfg_secondary_link', ''),
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




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.text import slugify
from .models import Page


@login_required
def page_list(request):
    tenant = request.tenant
    pages = Page.objects.filter(tenant=tenant)

    edit_obj = None

    if request.method == "POST":
        action = request.POST.get("action")

        # CREATE
        if action == "create":
            Page.objects.create(
                tenant=tenant,
                title=request.POST.get("title", "").strip(),
                slug=slugify(request.POST.get("slug", "").strip()),
                content=request.POST.get("content", ""),
                meta_description=request.POST.get("meta_description", "").strip(),
                published="published" in request.POST,
                show_in_footer="show_in_footer" in request.POST,
            )
            messages.success(request, "Page created.")
            return redirect("content:page_list")

        # UPDATE
        elif action == "update":
            pk = request.POST.get("page_id")
            page = get_object_or_404(Page, pk=pk, tenant=tenant)

            page.title = request.POST.get("title", "").strip()
            page.slug = slugify(request.POST.get("slug", "").strip())
            page.content = request.POST.get("content", "")
            page.meta_description = request.POST.get("meta_description", "").strip()
            page.published = "published" in request.POST
            page.show_in_footer = "show_in_footer" in request.POST
            page.save()

            messages.success(request, "Page updated.")
            return redirect("content:page_list")

        # DELETE
        elif action == "delete":
            pk = request.POST.get("page_id")
            page = get_object_or_404(Page, pk=pk, tenant=tenant)
            page.delete()
            messages.success(request, "Page deleted.")
            return redirect("content:page_list")

        # TOGGLE PUBLISH
        elif action == "toggle":
            pk = request.POST.get("page_id")
            page = get_object_or_404(Page, pk=pk, tenant=tenant)
            page.published = not page.published
            page.save()
            return redirect("content:page_list")

    # EDIT MODE
    edit_id = request.GET.get("edit")
    if edit_id:
        edit_obj = get_object_or_404(Page, pk=edit_id, tenant=tenant)

    context = {
        "pages": pages,
        "edit_obj": edit_obj,
        **build_nav_context(request),
    }

    return render(request, "dashboard/content/page_list.html", context)