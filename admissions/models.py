from django.db import models
from tenants.models import Tenant

class AdmissionForm(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='admission_forms')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='admission_forms/')
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title