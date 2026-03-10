# dashboard/views_programs.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from django.utils.text import slugify
from cache.models import CachedProgram
from .views import build_nav_context

@login_required
def dashboard_program_list(request):
    """Display list of all programs"""
    tenant = request.tenant
    
    # Get filter parameters
    status = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    
    # Base queryset
    program_list = CachedProgram.objects.filter(tenant=tenant)
    
    # Apply status filter
    if status == 'published':
        program_list = program_list.filter(is_published=True)
    elif status == 'draft':
        program_list = program_list.filter(is_published=False)
    
    # Apply search
    if search:
        program_list = program_list.filter(name__icontains=search)
    
    # Order by order field then name
    program_list = program_list.order_by('order', 'name')
    
    # Pagination
    paginator = Paginator(program_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_count = CachedProgram.objects.filter(tenant=tenant).count()
    published_count = CachedProgram.objects.filter(tenant=tenant, is_published=True).count()
    draft_count = CachedProgram.objects.filter(tenant=tenant, is_published=False).count()
    
    context = {
        'page_obj': page_obj,
        'program_count': program_list.count(),
        'total_count': total_count,
        'published_count': published_count,
        'draft_count': draft_count,
        'current_status': status,
        'search_query': search,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/programs/list.html', context)


@login_required
def dashboard_program_create(request):
    """Create a new program"""
    tenant = request.tenant
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        icon = request.POST.get('icon', '').strip()
        featured_image = request.POST.get('featured_image', '').strip()
        order = request.POST.get('order', 0)
        action = request.POST.get('action', 'draft')
        
        # Create program
        program = CachedProgram.objects.create(
            tenant=tenant,
            name=name,
            description=description,
            icon=icon,
            featured_image=featured_image,
            order=order,
            is_published=(action == 'publish'),
            last_synced=timezone.now(),
            sms_id=f"temp_{timezone.now().timestamp()}",  # Temporary ID
        )
        
        return redirect('/dashboard/programs/')
    
    context = {
        'tenant': tenant,
        'is_create': True,
        'now': timezone.now(),
        **build_nav_context(request),
    }
    return render(request, 'dashboard/programs/create.html', context)


@login_required
def dashboard_program_edit(request, program_id):
    """Edit an existing program"""
    tenant = request.tenant
    program = get_object_or_404(CachedProgram, id=program_id, tenant=tenant)
    
    if request.method == 'POST':
        # Update fields
        program.name = request.POST.get('name', program.name).strip()
        program.description = request.POST.get('description', program.description).strip()
        program.order = request.POST.get('order', program.order)
        
        # Handle icon
        if request.POST.get('remove_icon') == 'true':
            program.icon = ''
        elif request.POST.get('icon'):
            program.icon = request.POST.get('icon')
        
        # Handle featured image
        if request.POST.get('remove_featured_image') == 'true':
            program.featured_image = ''
        elif request.POST.get('featured_image'):
            program.featured_image = request.POST.get('featured_image')
        
        # Handle publish status
        action = request.POST.get('action', 'draft')
        if action == 'publish' and not program.is_published:
            program.is_published = True
        elif action == 'draft' and program.is_published:
            program.is_published = False
        
        program.last_synced = timezone.now()
        program.save()
        
        return redirect('/dashboard/programs/')
    
    context = {
        'program': program,
        'tenant': tenant,
        'is_create': False,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/programs/edit.html', context)


@login_required
def dashboard_program_delete(request, program_id):
    """Delete a program"""
    tenant = request.tenant
    program = get_object_or_404(CachedProgram, id=program_id, tenant=tenant)
    
    if request.method == 'POST':
        program.delete()
        return redirect('/dashboard/programs/')
    
    context = {
        'program': program,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/programs/delete.html', context)


@login_required
def dashboard_program_bulk_action(request):
    """Handle bulk actions on programs"""
    if request.method == 'POST':
        action = request.POST.get('action')
        program_ids = request.POST.getlist('program_ids')
        
        tenant = request.tenant
        programs = CachedProgram.objects.filter(tenant=tenant, id__in=program_ids)
        
        if action == 'publish':
            programs.update(is_published=True, last_synced=timezone.now())
        elif action == 'unpublish':
            programs.update(is_published=False, last_synced=timezone.now())
        elif action == 'delete':
            programs.delete()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def dashboard_program_reorder(request):
    """Handle reordering of programs"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        ordered_ids = data.get('ordered_ids', [])
        
        tenant = request.tenant
        for index, program_id in enumerate(ordered_ids):
            CachedProgram.objects.filter(tenant=tenant, id=program_id).update(order=index)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)