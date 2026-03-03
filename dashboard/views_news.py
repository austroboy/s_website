# dashboard/views_news.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.text import slugify
from django.http import JsonResponse
from cache.models import CachedNews
from .views import build_nav_context
import json

@login_required
def dashboard_news_list(request):
    """Display list of all news articles"""
    tenant = request.tenant
    
    # Get filter parameters
    status = request.GET.get('status', 'all')
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    
    # Base queryset
    news_list = CachedNews.objects.filter(tenant=tenant)
    
    # Apply filters
    if status == 'published':
        news_list = news_list.filter(is_published=True)
    elif status == 'draft':
        news_list = news_list.filter(is_published=False)
    
    if category:
        news_list = news_list.filter(category=category)
    
    if search:
        news_list = news_list.filter(title__icontains=search)
    
    # Order by most recent first
    news_list = news_list.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(news_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique categories for filter dropdown
    categories = CachedNews.objects.filter(tenant=tenant)\
                                   .exclude(category='')\
                                   .values_list('category', flat=True)\
                                   .distinct()
    
    context = {
        'page_obj': page_obj,
        'news_count': news_list.count(),
        'total_count': CachedNews.objects.filter(tenant=tenant).count(),
        'published_count': CachedNews.objects.filter(tenant=tenant, is_published=True).count(),
        'draft_count': CachedNews.objects.filter(tenant=tenant, is_published=False).count(),
        'categories': categories,
        'current_status': status,
        'current_category': category,
        'search_query': search,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/news/list.html', context)

@login_required
def dashboard_news_create(request):
    """Create a new news article"""
    tenant = request.tenant
    
    if request.method == 'POST':
        
        # Get form data
        title = request.POST.get('title', '').strip()
        summary = request.POST.get('summary', '').strip()
        content = request.POST.get('content', '').strip()
        slug = request.POST.get('slug', '').strip()
        category = request.POST.get('category', '').strip()
        author_name = request.POST.get('author_name', '').strip() or request.user.get_full_name() or request.user.username
        tags = request.POST.get('tags', '')
        featured_image = request.POST.get('featured_image', '') # URL from input
        action = request.POST.get('action', 'draft')
        
        # Handle tags (comma-separated to list)
        tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # Generate slug if not provided
        if not slug:
            slug = slugify(title)
        
        # Ensure slug is unique
        base_slug = slug
        counter = 1
        while CachedNews.objects.filter(tenant=tenant, slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Create news article
        news = CachedNews.objects.create(
            tenant=tenant,
            title=title,
            summary=summary,
            content=content,
            slug=slug,
            category=category,
            author_name=author_name,
            tags=tags_list,
            featured_image=featured_image,  # Save the URL directly
            is_published=(action == 'publish'),
            created_at=timezone.now(),
            updated_at=timezone.now(),
            sms_id=f"temp_{timezone.now().timestamp()}",  # Temporary ID
        )
        
        return redirect('/dashboard/news/')
    
    context = {
        'tenant': tenant,
        'is_create': True,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/news/create.html', context)


@login_required
def dashboard_news_edit(request, news_id):
    """Edit an existing news article"""
    tenant = request.tenant
    news = get_object_or_404(CachedNews, id=news_id, tenant=tenant)
    
    if request.method == 'POST':
        # Update fields
        news.title = request.POST.get('title', news.title).strip()
        news.summary = request.POST.get('summary', news.summary).strip()
        news.content = request.POST.get('content', news.content).strip()
        news.category = request.POST.get('category', news.category).strip()
        news.author_name = request.POST.get('author_name', news.author_name).strip()
        
        # Handle slug
        new_slug = request.POST.get('slug', '').strip()
        if new_slug and new_slug != news.slug:
            base_slug = new_slug
            counter = 1
            while CachedNews.objects.filter(tenant=tenant, slug=new_slug).exclude(id=news.id).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            news.slug = new_slug
        
        # Handle tags
        tags = request.POST.get('tags', '')
        news.tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # Handle featured image
        if request.POST.get('remove_image') == 'true':
            news.featured_image = ''
        else:
            new_image = request.POST.get('featured_image', '').strip()
            if new_image:
                news.featured_image = new_image
        
        # Handle publish status
        action = request.POST.get('action', 'draft')
        if action == 'publish' and not news.is_published:
            news.is_published = True
        elif action == 'draft' and news.is_published:
            news.is_published = False
        
        news.updated_at = timezone.now()
        news.save()
        
        return redirect('/dashboard/news/')
    
    # Convert tags list to comma-separated string for form
    tags_string = ', '.join(news.tags) if news.tags else ''
    
    context = {
        'news': news,
        'tags_string': tags_string,
        'tenant': tenant,
        'is_create': False,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/news/edit.html', context)


@login_required
def dashboard_news_delete(request, news_id):
    """Delete a news article"""
    tenant = request.tenant
    news = get_object_or_404(CachedNews, id=news_id, tenant=tenant)
    
    if request.method == 'POST':
        news.delete()
        return redirect('/dashboard/news/')
    
    context = {
        'news': news,
        'tenant': tenant,
        **build_nav_context(request),
    }
    return render(request, 'dashboard/news/delete.html', context)


@login_required
def dashboard_news_bulk_action(request):
    """Handle bulk actions on news articles"""
    if request.method == 'POST':
        action = request.POST.get('action')
        news_ids = request.POST.getlist('news_ids')
        
        tenant = request.tenant
        news_items = CachedNews.objects.filter(tenant=tenant, id__in=news_ids)
        
        if action == 'publish':
            news_items.update(is_published=True, updated_at=timezone.now())
        elif action == 'unpublish':
            news_items.update(is_published=False, updated_at=timezone.now())
        elif action == 'delete':
            news_items.delete()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def dashboard_news_preview(request, news_id):
    """Preview a news article"""
    tenant = request.tenant
    news = get_object_or_404(CachedNews, id=news_id, tenant=tenant)
    
    context = {
        'news': news,
        'tenant': tenant,
        'is_preview': True,
    }
    return render(request, 'dashboard/news/preview.html', context)