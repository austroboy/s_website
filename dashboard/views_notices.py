# dashboard/views_notices.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.text import slugify
from django.http import JsonResponse
from cache.models import CachedNotice
from .views import build_nav_context


@login_required
def dashboard_notice_list(request):
    """Display list of all notices"""
    tenant = request.tenant

    status = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    expiry_filter = request.GET.get('expiry', '')

    notice_list = CachedNotice.objects.filter(tenant=tenant)

    if status == 'published':
        notice_list = notice_list.filter(is_published=True)
    elif status == 'draft':
        notice_list = notice_list.filter(is_published=False)

    if expiry_filter == 'active':
        notice_list = notice_list.filter(expiry_date__gte=timezone.now().date())
    elif expiry_filter == 'expired':
        notice_list = notice_list.filter(expiry_date__lt=timezone.now().date())
    elif expiry_filter == 'no_expiry':
        notice_list = notice_list.filter(expiry_date__isnull=True)

    if search:
        notice_list = notice_list.filter(title__icontains=search)

    notice_list = notice_list.order_by('-created_at')

    paginator = Paginator(notice_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    today = timezone.now().date()

    context = {
        'page_obj': page_obj,
        'notice_count': notice_list.count(),
        'total_count': CachedNotice.objects.filter(tenant=tenant).count(),
        'published_count': CachedNotice.objects.filter(tenant=tenant, is_published=True).count(),
        'draft_count': CachedNotice.objects.filter(tenant=tenant, is_published=False).count(),
        'active_count': CachedNotice.objects.filter(
            tenant=tenant, is_published=True, expiry_date__gte=today
        ).count(),
        'current_status': status,
        'current_expiry': expiry_filter,
        'search_query': search,
        'tenant': tenant,
        'today': today,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/notices/list.html', context)


@login_required
def dashboard_notice_create(request):
    """Create a new notice"""
    tenant = request.tenant

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        summary = request.POST.get('summary', '').strip()
        content = request.POST.get('content', '').strip()
        slug = request.POST.get('slug', '').strip()
        featured_image = request.POST.get('featured_image', '').strip()
        attachment_url = request.POST.get('attachment_url', '').strip()
        expiry_date = request.POST.get('expiry_date', '').strip() or None
        action = request.POST.get('action', 'draft')

        if not slug:
            slug = slugify(title)

        base_slug = slug
        counter = 1
        while CachedNotice.objects.filter(tenant=tenant, slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        CachedNotice.objects.create(
            tenant=tenant,
            title=title,
            summary=summary,
            content=content,
            slug=slug,
            featured_image=featured_image,
            attachment_url=attachment_url,
            expiry_date=expiry_date,
            is_published=(action == 'publish'),
            created_at=timezone.now(),
            updated_at=timezone.now(),
            sms_id=f"temp_{timezone.now().timestamp()}",
        )

        return redirect('/dashboard/notices/')

    context = {
        'tenant': tenant,
        'is_create': True,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/notices/create.html', context)


@login_required
def dashboard_notice_edit(request, notice_id):
    """Edit an existing notice"""
    tenant = request.tenant
    notice = get_object_or_404(CachedNotice, id=notice_id, tenant=tenant)

    if request.method == 'POST':
        notice.title = request.POST.get('title', notice.title).strip()
        notice.summary = request.POST.get('summary', notice.summary).strip()
        notice.content = request.POST.get('content', notice.content).strip()
        notice.attachment_url = request.POST.get('attachment_url', notice.attachment_url).strip()
        expiry_date = request.POST.get('expiry_date', '').strip()
        notice.expiry_date = expiry_date if expiry_date else None

        new_slug = request.POST.get('slug', '').strip()
        if new_slug and new_slug != notice.slug:
            base_slug = new_slug
            counter = 1
            while CachedNotice.objects.filter(tenant=tenant, slug=new_slug).exclude(id=notice.id).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            notice.slug = new_slug

        # Handle featured image URL
        if request.POST.get('remove_image') == 'true':
            notice.featured_image = ''
        elif request.POST.get('featured_image'):
            notice.featured_image = request.POST.get('featured_image').strip()

        action = request.POST.get('action', 'draft')
        notice.is_published = (action == 'publish')
        notice.updated_at = timezone.now()
        notice.save()

        return redirect('/dashboard/notices/')

    context = {
        'notice': notice,
        'tenant': tenant,
        'is_create': False,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/notices/edit.html', context)


@login_required
def dashboard_notice_delete(request, notice_id):
    """Delete a notice"""
    tenant = request.tenant
    notice = get_object_or_404(CachedNotice, id=notice_id, tenant=tenant)

    if request.method == 'POST':
        notice.delete()
        return redirect('/dashboard/notices/')

    context = {
        'notice': notice,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/notices/delete.html', context)


@login_required
def dashboard_notice_bulk_action(request):
    """Handle bulk actions on notices"""
    if request.method == 'POST':
        action = request.POST.get('action')
        notice_ids = request.POST.getlist('notice_ids')
        tenant = request.tenant
        notices = CachedNotice.objects.filter(tenant=tenant, id__in=notice_ids)

        if action == 'publish':
            notices.update(is_published=True, updated_at=timezone.now())
        elif action == 'unpublish':
            notices.update(is_published=False, updated_at=timezone.now())
        elif action == 'delete':
            notices.delete()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@login_required
def dashboard_notice_preview(request, notice_id):
    """Preview a notice"""
    tenant = request.tenant
    notice = get_object_or_404(CachedNotice, id=notice_id, tenant=tenant)

    context = {
        'notice': notice,
        'tenant': tenant,
        'is_preview': True,
    }
    return render(request, 'dashboard/notices/preview.html', context)