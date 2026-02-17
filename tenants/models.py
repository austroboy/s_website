from django.db import models
from django.utils import timezone

class Tenant(models.Model):
    """
    Represents one school customer.
    Data is pulled from SMS using the tenant_id and API credentials.
    """
    # ID used in SMS – can be an integer or UUID
    sms_tenant_id = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    subdomain = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # API authentication for this tenant (store encrypted)
    api_base_url = models.URLField(help_text="SMS API base URL for this tenant")
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)

    # Feature flags – which modules are active on the website
    enable_news = models.BooleanField(default=True)
    enable_events = models.BooleanField(default=True)
    enable_notices = models.BooleanField(default=True)
    enable_staff_directory = models.BooleanField(default=True)
    enable_gallery = models.BooleanField(default=True)
    enable_admissions = models.BooleanField(default=True)
    enable_results = models.BooleanField(default=True)

    # Contact info (can be overridden locally)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Domain(models.Model):
    """
    Maps a domain name to a tenant.
    One tenant can have multiple domains (e.g. www and bare).
    """
    domain = models.CharField(max_length=253, unique=True, db_index=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='domains')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain