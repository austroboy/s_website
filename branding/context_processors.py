# branding/context_processors.py
from .models import ColorPalette, FontPair, BrandAssets

def branding(request):
    """
    Injects tenant-specific branding data into all templates.
    """
    if hasattr(request, 'tenant'):
        # Get or create default objects (they will not be saved to DB unless explicitly saved)
        colors, _ = ColorPalette.objects.get_or_create(tenant=request.tenant)
        fonts, _ = FontPair.objects.get_or_create(tenant=request.tenant)
        assets, _ = BrandAssets.objects.get_or_create(tenant=request.tenant)
        return {
            'colors': colors,
            'fonts': fonts,
            'assets': assets,
        }
    # Return empty dict if no tenant (e.g., admin pages)
    return {}