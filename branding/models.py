from django.db import models
from tenants.models import Tenant

class ColorPalette(models.Model):
    """
    Token‑based colour system.
    Tokens are used in CSS variables.
    """
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='colors')
    primary = models.CharField(max_length=7, default='#0A4D8C')       # main brand colour
    secondary = models.CharField(max_length=7, default='#E67E22')     # accent
    accent = models.CharField(max_length=7, default='#2ECC71')        # highlight
    surface = models.CharField(max_length=7, default='#FFFFFF')       # background / card
    text = models.CharField(max_length=7, default='#1A1A1A')          # body text
    text_muted = models.CharField(max_length=7, default='#6C757D')    # secondary text
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