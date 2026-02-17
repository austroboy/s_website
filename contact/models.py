from django.db import models
from tenants.models import Tenant

class ContactSubmission(models.Model):
    """
    Messages from the contact form.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='contact_submissions')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.tenant.name}] {self.name} - {self.subject}"


class AdmissionInquiry(models.Model):
    """
    Prospective student inquiry.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='admission_inquiries')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    program_of_interest = models.CharField(max_length=200, blank=True)
    grade_level = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.tenant.name}] {self.full_name}"