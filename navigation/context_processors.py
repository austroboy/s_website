# navigation/context_processors.py
from .models import Menu

def menus(request):
    """
    Injects header and footer menus for the current tenant.
    """
    if hasattr(request, 'tenant'):
        try:
            header_menu = Menu.objects.get(tenant=request.tenant, slug='header')
            # We need to prefetch children for efficiency
            from django.db.models import Prefetch
            header_items = header_menu.items.filter(is_active=True).order_by('order').prefetch_related(
                Prefetch('children', queryset=MenuItem.objects.filter(is_active=True).order_by('order'))
            )
            footer_menu = Menu.objects.get(tenant=request.tenant, slug='footer')
            footer_items = footer_menu.items.filter(is_active=True).order_by('order')
            return {
                'menus': {
                    'header': header_items,
                    'footer': footer_items,
                }
            }
        except Menu.DoesNotExist:
            pass
    return {'menus': {'header': [], 'footer': []}}