# dashboard/views_staff.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from cache.models import CachedStaff
from .views import build_nav_context
from django.db import models

@login_required
def dashboard_staff_list(request):
    """Display list of all staff members"""
    tenant = request.tenant
    
    # Get filter parameters
    status = request.GET.get('status', 'all')
    department = request.GET.get('department', '')
    search = request.GET.get('search', '')
    
    # Base queryset
    staff_list = CachedStaff.objects.filter(tenant=tenant)
    
    # Apply status filter
    if status == 'published':
        staff_list = staff_list.filter(is_published=True)
    elif status == 'draft':
        staff_list = staff_list.filter(is_published=False)
    
    # Apply department filter
    if department:
        staff_list = staff_list.filter(department=department)
    
    # Apply search
    if search:
        staff_list = staff_list.filter(
            models.Q(name__icontains=search) | 
            models.Q(designation__icontains=search) |
            models.Q(department__icontains=search) |
            models.Q(email__icontains=search)
        )
    
    # Order by order field then name
    staff_list = staff_list.order_by('order', 'name')
    
    # Pagination
    paginator = Paginator(staff_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique departments for filter dropdown
    departments = CachedStaff.objects.filter(tenant=tenant)\
                                   .exclude(department='')\
                                   .values_list('department', flat=True)\
                                   .distinct().order_by('department')
    
    # Statistics
    total_count = CachedStaff.objects.filter(tenant=tenant).count()
    published_count = CachedStaff.objects.filter(tenant=tenant, is_published=True).count()
    draft_count = CachedStaff.objects.filter(tenant=tenant, is_published=False).count()
    
    context = {
        'page_obj': page_obj,
        'staff_count': staff_list.count(),
        'total_count': total_count,
        'published_count': published_count,
        'draft_count': draft_count,
        'departments': departments,
        'current_status': status,
        'current_department': department,
        'search_query': search,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/staff/list.html', context)


@login_required
def dashboard_staff_create(request):
    """Create a new staff member"""
    tenant = request.tenant
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        designation = request.POST.get('designation', '').strip()
        department = request.POST.get('department', '').strip()
        bio = request.POST.get('bio', '').strip()
        photo = request.POST.get('photo', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        order = request.POST.get('order', 0)
        action = request.POST.get('action', 'draft')
        
        # Create staff member
        staff = CachedStaff.objects.create(
            tenant=tenant,
            name=name,
            designation=designation,
            department=department,
            bio=bio,
            photo=photo,
            email=email,
            phone=phone,
            order=order,
            is_published=(action == 'publish'),
            last_synced=timezone.now(),
            sms_id=f"temp_{timezone.now().timestamp()}",  # Temporary ID
        )
        
        return redirect('/dashboard/staff/')
    
    # Get departments for dropdown
    departments = CachedStaff.objects.filter(tenant=tenant)\
                                   .exclude(department='')\
                                   .values_list('department', flat=True)\
                                   .distinct().order_by('department')
    
    context = {
        'tenant': tenant,
        'departments': departments,
        'is_create': True,
        'now': timezone.now(),
        **build_nav_context(request),
    }
    return render(request, 'dashboard/staff/create.html', context)


@login_required
def dashboard_staff_edit(request, staff_id):
    """Edit an existing staff member"""
    tenant = request.tenant
    staff = get_object_or_404(CachedStaff, id=staff_id, tenant=tenant)
    
    if request.method == 'POST':
        # Update fields
        staff.name = request.POST.get('name', staff.name).strip()
        staff.designation = request.POST.get('designation', staff.designation).strip()
        staff.department = request.POST.get('department', staff.department).strip()
        staff.bio = request.POST.get('bio', staff.bio).strip()
        staff.email = request.POST.get('email', staff.email).strip()
        staff.phone = request.POST.get('phone', staff.phone).strip()
        staff.order = request.POST.get('order', staff.order)
        
        # Handle photo
        if request.POST.get('remove_photo') == 'true':
            staff.photo = ''
        elif request.POST.get('photo'):
            staff.photo = request.POST.get('photo')
        
        # Handle publish status
        action = request.POST.get('action', 'draft')
        if action == 'publish' and not staff.is_published:
            staff.is_published = True
        elif action == 'draft' and staff.is_published:
            staff.is_published = False
        
        staff.last_synced = timezone.now()
        staff.save()
        
        return redirect('/dashboard/staff/')
    
    # Get departments for dropdown
    departments = CachedStaff.objects.filter(tenant=tenant)\
                                   .exclude(department='')\
                                   .values_list('department', flat=True)\
                                   .distinct().order_by('department')
    
    context = {
        'staff': staff,
        'departments': departments,
        'tenant': tenant,
        'is_create': False,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/staff/edit.html', context)


@login_required
def dashboard_staff_delete(request, staff_id):
    """Delete a staff member"""
    tenant = request.tenant
    staff = get_object_or_404(CachedStaff, id=staff_id, tenant=tenant)
    
    if request.method == 'POST':
        staff.delete()
        return redirect('/dashboard/staff/')
    
    context = {
        'staff': staff,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/staff/delete.html', context)


@login_required
def dashboard_staff_bulk_action(request):
    """Handle bulk actions on staff members"""
    if request.method == 'POST':
        action = request.POST.get('action')
        staff_ids = request.POST.getlist('staff_ids')
        
        tenant = request.tenant
        staff_members = CachedStaff.objects.filter(tenant=tenant, id__in=staff_ids)
        
        if action == 'publish':
            staff_members.update(is_published=True, last_synced=timezone.now())
        elif action == 'unpublish':
            staff_members.update(is_published=False, last_synced=timezone.now())
        elif action == 'delete':
            staff_members.delete()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def dashboard_staff_reorder(request):
    """Handle reordering of staff members"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        ordered_ids = data.get('ordered_ids', [])
        
        tenant = request.tenant
        for index, staff_id in enumerate(ordered_ids):
            CachedStaff.objects.filter(tenant=tenant, id=staff_id).update(order=index)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)