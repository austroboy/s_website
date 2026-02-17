from django.db import models
from tenants.models import Tenant

class Achievement(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-date']

    def __str__(self):
        return self.title