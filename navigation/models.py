from django.db import models
from tenants.models import Tenant

class Menu(models.Model):
    """
    A named menu (e.g. 'header', 'footer', 'sidebar').
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=100)
    slug = models.SlugField(help_text="Unique identifier for this menu")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenant', 'slug')

    def __str__(self):
        return f"{self.tenant.name} - {self.name}"


class MenuItem(models.Model):
    """
    An item in a menu, supporting nested structure.
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500, blank=True, help_text="External or internal path")
    page = models.ForeignKey('content.Page', on_delete=models.SET_NULL, null=True, blank=True, help_text="Link to a local page")
    order = models.PositiveIntegerField(default=0)
    target_blank = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title