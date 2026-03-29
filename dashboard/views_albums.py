import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import F
from cache.models import CachedAlbum, AlbumMedia
from .views import build_nav_context

@login_required
def dashboard_album_list(request):
    """Display list of all albums"""
    tenant = request.tenant
    
    # Get filter parameters
    status = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    
    # Base queryset
    album_list = CachedAlbum.objects.filter(tenant=tenant)
    
    # Apply status filter
    if status == 'published':
        album_list = album_list.filter(is_published=True)
    elif status == 'draft':
        album_list = album_list.filter(is_published=False)
    
    # Apply search
    if search:
        album_list = album_list.filter(title__icontains=search)
    
    # Order by created_at (most recent first)
    album_list = album_list.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(album_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_count = CachedAlbum.objects.filter(tenant=tenant).count()
    published_count = CachedAlbum.objects.filter(tenant=tenant, is_published=True).count()
    draft_count = CachedAlbum.objects.filter(tenant=tenant, is_published=False).count()
    
    # Calculate total media items across all albums
    total_media = AlbumMedia.objects.filter(album__tenant=tenant).count()
    
    context = {
        'page_obj': page_obj,
        'album_count': album_list.count(),
        'total_count': total_count,
        'published_count': published_count,
        'draft_count': draft_count,
        'total_media': total_media,
        'current_status': status,
        'search_query': search,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/albums/list.html', context)


@login_required
def dashboard_album_create(request):
    """Create a new album"""
    tenant = request.tenant
    
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        action = request.POST.get('action', 'draft')
        
        # Create album
        album = CachedAlbum.objects.create(
            tenant=tenant,
            title=title,
            description=description,
            cover_image=request.FILES.get('cover_image'),
            is_published=(action == 'publish'),
            created_at=timezone.now(),
            last_synced=timezone.now(),
            sms_id=f"temp_{timezone.now().timestamp()}",
        )
        
        # Handle local media items
        media_ids_json = request.POST.get('local_media_ids', '[]')
        try:
            media_ids = json.loads(media_ids_json)
            for index, m_id in enumerate(media_ids):
                AlbumMedia.objects.filter(id=m_id).update(album=album, order=index)
        except:
            pass
            
        # Also handle legacy URL media if needed
        media_items_json = request.POST.get('media_items', '[]')
        try:
            album.media_items = json.loads(media_items_json)
            album.save()
        except:
            pass
        
        return redirect('/dashboard/albums/')
    
    context = {
        'tenant': tenant,
        'is_create': True,
        'now': timezone.now(),
        **build_nav_context(request),
    }
    return render(request, 'dashboard/albums/create.html', context)


@login_required
def dashboard_album_edit(request, album_id):
    """Edit an existing album"""
    tenant = request.tenant
    album = get_object_or_404(CachedAlbum, id=album_id, tenant=tenant)
    
    if request.method == 'POST':
        # Update fields
        album.title = request.POST.get('title', album.title).strip()
        album.description = request.POST.get('description', album.description).strip()
        
        # Handle cover image
        if request.POST.get('remove_cover_image') == 'true':
            album.cover_image = None
        
        new_cover = request.FILES.get('cover_image')
        if new_cover:
            album.cover_image = new_cover
        
        # Handle local media items reordering and assignment
        media_ids_json = request.POST.get('local_media_ids', '[]')
        try:
            media_ids = json.loads(media_ids_json)
            # Remove items not in the list
            album.local_media.exclude(id__in=media_ids).delete()
            # Update order and ensure assignment
            for index, m_id in enumerate(media_ids):
                AlbumMedia.objects.filter(id=m_id).update(album=album, order=index)
        except:
            pass

        # Handle legacy URL media items
        media_items_json = request.POST.get('media_items', '[]')
        try:
            album.media_items = json.loads(media_items_json)
        except:
            pass
            
        # Handle publish status
        action = request.POST.get('action', 'draft')
        album.is_published = (action == 'publish')
        
        album.last_synced = timezone.now()
        album.save()
        
        return redirect('/dashboard/albums/')
    
    # Get existing local media
    local_media = album.local_media.all()
    local_media_list = []
    for m in local_media:
        local_media_list.append({
            'id': m.id,
            'url': m.file.url,
            'type': m.media_type,
            'caption': m.caption
        })
    
    context = {
        'album': album,
        'media_items_json': json.dumps(album.media_items),
        'local_media_json': json.dumps(local_media_list),
        'tenant': tenant,
        'is_create': False,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/albums/edit.html', context)


@login_required
def dashboard_album_delete(request, album_id):
    """Delete an album"""
    tenant = request.tenant
    album = get_object_or_404(CachedAlbum, id=album_id, tenant=tenant)
    
    if request.method == 'POST':
        album.delete()
        return redirect('/dashboard/albums/')
    
    context = {
        'album': album,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/albums/delete.html', context)


@login_required
def dashboard_album_preview(request, album_id):
    """Preview an album"""
    tenant = request.tenant
    album = get_object_or_404(CachedAlbum, id=album_id, tenant=tenant)
    
    context = {
        'album': album,
        'tenant': tenant,
        'is_preview': True,
    }
    return render(request, 'dashboard/albums/preview.html', context)


@login_required
def dashboard_album_bulk_action(request):
    """Handle bulk actions on albums"""
    if request.method == 'POST':
        action = request.POST.get('action')
        album_ids = request.POST.getlist('album_ids')
        
        tenant = request.tenant
        albums = CachedAlbum.objects.filter(tenant=tenant, id__in=album_ids)
        
        if action == 'publish':
            albums.update(is_published=True, last_synced=timezone.now())
        elif action == 'unpublish':
            albums.update(is_published=False, last_synced=timezone.now())
        elif action == 'delete':
            albums.delete()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def dashboard_album_upload_media(request):
    """Handle media upload for albums via AJAX"""
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        # Determine media type
        ext = file.name.split('.')[-1].lower()
        media_type = 'image'
        if ext in ['mp4', 'webm', 'ogg', 'mov']:
            media_type = 'video'
            
        media = AlbumMedia.objects.create(
            file=file,
            media_type=media_type,
            order=999 # Temporary order
        )
        
        return JsonResponse({
            'status': 'success',
            'id': media.id,
            'url': media.file.url,
            'type': media.media_type,
            'name': file.name
        })
    
    return JsonResponse({'status': 'error'}, status=400)
