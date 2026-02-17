from django.db import models
from tenants.models import Tenant

class Page(models.Model):
    """
    Static pages like About, Contact, etc. that may have custom content.
    (Most pages will be dynamic from SMS, but we offer local override.)
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField(help_text="HTML content (safe tags allowed)")
    meta_description = models.CharField(max_length=300, blank=True)
    published = models.BooleanField(default=False)
    show_in_footer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tenant', 'slug')

    def __str__(self):
        return f"{self.tenant.name} - {self.title}"


class HomepageSection(models.Model):
    """
    Each section of the homepage can be enabled, ordered, and configured.
    Section type determines which template to render.
    """
    SECTION_TYPES = [
        ('hero', 'Hero with CTA'),
        ('features', 'Features/Programs Grid'),
        ('stats', 'Statistics/Highlights'),
        ('news', 'Latest News'),
        ('events', 'Upcoming Events'),
        ('notices', 'Important Notices'),
        ('testimonials', 'Testimonials'),
        ('gallery', 'Gallery'),
        ('cta', 'Call to Action'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='homepage_sections')
    section_type = models.CharField(max_length=30, choices=SECTION_TYPES)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    # JSON configuration for the section (e.g. number of items to show)
    config = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.tenant.name} - {self.get_section_type_display()}"