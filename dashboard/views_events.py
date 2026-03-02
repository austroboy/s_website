# dashboard/views_events.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.text import slugify
from django.http import JsonResponse
from datetime import datetime
from cache.models import CachedEvent
from .views import build_nav_context

@login_required
def dashboard_event_list(request):
    """Display list of all events"""
    tenant = request.tenant
    
    # Get filter parameters
    status = request.GET.get('status', 'all')
    date_filter = request.GET.get('date', 'all')
    search = request.GET.get('search', '')
    
    # Base queryset
    event_list = CachedEvent.objects.filter(tenant=tenant)
    
    # Apply status filter
    if status == 'published':
        event_list = event_list.filter(is_published=True)
    elif status == 'draft':
        event_list = event_list.filter(is_published=False)
    
    # Apply date filter
    today = timezone.now()
    if date_filter == 'upcoming':
        event_list = event_list.filter(start_date__gte=today)
    elif date_filter == 'past':
        event_list = event_list.filter(start_date__lt=today)
    elif date_filter == 'this_week':
        week_end = today + timezone.timedelta(days=7)
        event_list = event_list.filter(start_date__range=[today, week_end])
    elif date_filter == 'this_month':
        month_end = today + timezone.timedelta(days=30)
        event_list = event_list.filter(start_date__range=[today, month_end])
    
    # Apply search
    if search:
        event_list = event_list.filter(title__icontains=search)
    
    # Order by start date (upcoming first)
    event_list = event_list.order_by('start_date')
    
    # Pagination
    paginator = Paginator(event_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_count = CachedEvent.objects.filter(tenant=tenant).count()
    published_count = CachedEvent.objects.filter(tenant=tenant, is_published=True).count()
    draft_count = CachedEvent.objects.filter(tenant=tenant, is_published=False).count()
    upcoming_count = CachedEvent.objects.filter(tenant=tenant, is_published=True, start_date__gte=today).count()
    
    context = {
        'page_obj': page_obj,
        'event_count': event_list.count(),
        'total_count': total_count,
        'published_count': published_count,
        'draft_count': draft_count,
        'upcoming_count': upcoming_count,
        'current_status': status,
        'current_date_filter': date_filter,
        'search_query': search,
        'today': today,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/events/list.html', context)


@login_required
def dashboard_event_create(request):
    """Create a new event"""
    tenant = request.tenant
    
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title', '').strip()
        summary = request.POST.get('summary', '').strip()
        content = request.POST.get('content', '').strip()
        slug = request.POST.get('slug', '').strip()
        
        # Date handling
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        # Parse dates
        try:
            start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            start_date = timezone.now()
            end_date = timezone.now() + timezone.timedelta(hours=2)
        
        venue = request.POST.get('venue', '').strip()
        registration_link = request.POST.get('registration_link', '').strip()
        action = request.POST.get('action', 'draft')
        
        # Generate slug if not provided
        if not slug:
            slug = slugify(title)
        
        # Ensure slug is unique
        base_slug = slug
        counter = 1
        while CachedEvent.objects.filter(tenant=tenant, slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Create event
        event = CachedEvent.objects.create(
            tenant=tenant,
            title=title,
            summary=summary,
            content=content,
            slug=slug,
            start_date=start_date,
            end_date=end_date,
            venue=venue,
            registration_link=registration_link,
            featured_image=request.POST.get('featured_image', ''),
            is_published=(action == 'publish'),
            created_at=timezone.now(),
            updated_at=timezone.now(),
            sms_id=f"temp_{timezone.now().timestamp()}",  # Temporary ID
        )
        
        return redirect('/dashboard/events/')
    
    context = {
        'tenant': tenant,
        'is_create': True,
        'now': timezone.now(),
        **build_nav_context(request),
    }
    return render(request, 'dashboard/events/create.html', context)


@login_required
def dashboard_event_edit(request, event_id):
    """Edit an existing event"""
    tenant = request.tenant
    event = get_object_or_404(CachedEvent, id=event_id, tenant=tenant)
    
    if request.method == 'POST':
        # Update fields
        event.title = request.POST.get('title', event.title).strip()
        event.summary = request.POST.get('summary', event.summary).strip()
        event.content = request.POST.get('content', event.content).strip()
        
        # Update dates
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        try:
            if start_date_str:
                event.start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            if end_date_str:
                event.end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            pass
        
        event.venue = request.POST.get('venue', event.venue).strip()
        event.registration_link = request.POST.get('registration_link', event.registration_link).strip()
        
        # Handle slug
        new_slug = request.POST.get('slug', '').strip()
        if new_slug and new_slug != event.slug:
            base_slug = new_slug
            counter = 1
            while CachedEvent.objects.filter(tenant=tenant, slug=new_slug).exclude(id=event.id).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            event.slug = new_slug
        
        # Handle publish status
        action = request.POST.get('action', 'draft')
        if action == 'publish' and not event.is_published:
            event.is_published = True
        elif action == 'draft' and event.is_published:
            event.is_published = False
        
        # Handle featured image
        if request.POST.get('remove_image') == 'true':
            event.featured_image = ''
        elif request.POST.get('featured_image'):
            event.featured_image = request.POST.get('featured_image')
        
        event.updated_at = timezone.now()
        event.save()
        
        return redirect('/dashboard/events/')
    
    context = {
        'event': event,
        'tenant': tenant,
        'is_create': False,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/events/edit.html', context)


@login_required
def dashboard_event_delete(request, event_id):
    """Delete an event"""
    tenant = request.tenant
    event = get_object_or_404(CachedEvent, id=event_id, tenant=tenant)
    
    if request.method == 'POST':
        event.delete()
        return redirect('/dashboard/events/')
    
    context = {
        'event': event,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/events/delete.html', context)


@login_required
def dashboard_event_preview(request, event_id):
    """Preview an event"""
    tenant = request.tenant
    event = get_object_or_404(CachedEvent, id=event_id, tenant=tenant)
    
    context = {
        'event': event,
        'tenant': tenant,
        'is_preview': True,
    }
    return render(request, 'dashboard/events/preview.html', context)


@login_required
def dashboard_event_bulk_action(request):
    """Handle bulk actions on events"""
    if request.method == 'POST':
        action = request.POST.get('action')
        event_ids = request.POST.getlist('event_ids')
        
        tenant = request.tenant
        events = CachedEvent.objects.filter(tenant=tenant, id__in=event_ids)
        
        if action == 'publish':
            events.update(is_published=True, updated_at=timezone.now())
        elif action == 'unpublish':
            events.update(is_published=False, updated_at=timezone.now())
        elif action == 'delete':
            events.delete()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)