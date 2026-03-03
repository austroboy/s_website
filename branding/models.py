from django.db import models
from tenants.models import Tenant

class ColorPalette(models.Model):
    """
    Token‑based colour system.
    Tokens are used in CSS variables.
    """
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='colors')
    primary = models.CharField(max_length=7, default='#0051FF')       # main brand colour
    primary_dark = models.CharField(max_length=7, default='#003ACC')
    primary_light = models.CharField(max_length=7, default='#3B82F6')
    primary_glow = models.CharField(max_length=50, default='rgba(0, 81, 255, 0.35)')
    
    secondary = models.CharField(max_length=7, default='#0F1D40')     # accent
    secondary_light = models.CharField(max_length=7, default='#1A2D5A')
    
    accent = models.CharField(max_length=7, default='#00D4FF')        # highlight
    surface = models.CharField(max_length=7, default='#F8FAFD')       # background / card
    text = models.CharField(max_length=7, default='#1A1A2E')          # body text
    text_muted = models.CharField(max_length=7, default='#64748B')    # secondary text
    surface_alt = models.CharField(max_length=7, default='#EFF4FB')   # alternate background
    footer_bg = models.CharField(max_length=7, default='#111827')     # footer background
    footer_text = models.CharField(max_length=7, default='#FFFFFF')   # footer text
    border = models.CharField(max_length=7, default='#E5E7EB')        # standard border
    success = models.CharField(max_length=7, default='#28A745')
    warning = models.CharField(max_length=7, default='#FFC107')
    error = models.CharField(max_length=7, default='#DC3545')

    # Dark mode overrides (optional)
    dark_primary = models.CharField(max_length=7, blank=True)
    dark_surface = models.CharField(max_length=7, blank=True)
    dark_text = models.CharField(max_length=7, blank=True)

    def __str__(self):
        return f"Colors for {self.tenant.name}"


class FontPair(models.Model):
    """
    Font choices for headings and body.
    """
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='fonts')
    heading_font = models.CharField(max_length=100, default='Inter')
    body_font = models.CharField(max_length=100, default='system-ui')
    # Google Fonts weights, fallbacks, etc.
    heading_weights = models.CharField(max_length=50, default='400,600,700')
    body_weights = models.CharField(max_length=50, default='400,500')

    @property
    def heading_weights_list(self):
        return [w.strip() for w in self.heading_weights.split(',')]

    @property
    def body_weights_list(self):
        return [w.strip() for w in self.body_weights.split(',')]

    def google_fonts_url(self):
        """Returns the full Google Fonts embed URL for this pair."""
        h = self.heading_font.replace(' ', '+')
        b = self.body_font.replace(' ', '+')
        hw = ';'.join(f'0,{w}' for w in self.heading_weights_list)
        bw = ';'.join(f'0,{w}' for w in self.body_weights_list)
        return (
            f'https://fonts.googleapis.com/css2?'
            f'family={h}:ital,wght@{hw}'
            f'&family={b}:ital,wght@{bw}'
            f'&display=swap'
        )

    def __str__(self):
        return f"Fonts for {self.tenant.name}"


class BrandAssets(models.Model):
    """
    Logos, favicon, social images.
    """
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='assets')
    logo_light = models.ImageField(upload_to='branding/%Y/%m/', blank=True)
    logo_dark = models.ImageField(upload_to='branding/%Y/%m/', blank=True)
    favicon = models.ImageField(upload_to='branding/', blank=True)
    og_image = models.ImageField(upload_to='branding/', blank=True, help_text="Default social sharing image")
    footer_logo = models.ImageField(upload_to='branding/', blank=True)

    def __str__(self):
        return f"Assets for {self.tenant.name}"