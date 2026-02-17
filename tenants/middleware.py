from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import Domain
from cache.managers import set_current_tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow admin, static, and media files without a tenant
        path = request.path_info.lstrip('/')
        if path.startswith('admin/') or path.startswith('static/') or path.startswith('media/'):
            return self.get_response(request)

        host = request.get_host().split(':')[0].lower()
        try:
            domain = Domain.objects.select_related('tenant').get(domain=host)
        except Domain.DoesNotExist:
            # Show a "Site Not Configured" page
            return HttpResponseNotFound(render(request, 'tenants/not_configured.html', status=404))

        request.tenant = domain.tenant
        set_current_tenant(domain.tenant)
        return self.get_response(request)