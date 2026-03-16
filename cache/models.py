from django.db import models
from tenants.models import Tenant
from .managers import TenantAwareManager

class BaseCachedModel(models.Model):
    """
    Abstract base for all cached models.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    sms_id = models.CharField(max_length=50, db_index=True, help_text="Original ID in SMS")
    last_synced = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    # Common fields
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='featured_images/', blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = TenantAwareManager()

    class Meta:
        abstract = True
        unique_together = ('tenant', 'sms_id')


class CachedNews(BaseCachedModel):
    """
    News articles.
    """
    author_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)  # array of strings
    objects = TenantAwareManager()

    def __str__(self):
        return f"[{self.tenant.name}] {self.title}"


class CachedEvent(BaseCachedModel):
    """
    Events.
    """
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=300, blank=True)
    registration_link = models.URLField(blank=True)

    def __str__(self):
        return f"[{self.tenant.name}] {self.title}"
















class CachedNotice(BaseCachedModel):
    """
    Urgent notices / announcements.
    """
    expiry_date = models.DateField(null=True, blank=True)
    attachment_url = models.FileField(upload_to='notices/', blank=True, null=True, help_text="Upload PDF etc.")

    def __str__(self):
        return f"[{self.tenant.name}] {self.title}"


class CachedStaff(models.Model):
    """
    Staff directory (public profiles only).
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    sms_id = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    department = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staff/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    last_synced = models.DateTimeField(auto_now=True)

    objects = TenantAwareManager()

    class Meta:
        unique_together = ('tenant', 'sms_id')
        ordering = ['order']

    def __str__(self):
        return f"[{self.tenant.name}] {self.name}"


class CachedProgram(models.Model):
    """
    Academic programs / classes / departments.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    sms_id = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='program_icons/', blank=True, null=True)
    featured_image = models.ImageField(upload_to='programs/', blank=True, null=True, help_text="Featured/banner image for this program")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    last_synced = models.DateTimeField(auto_now=True)

    objects = TenantAwareManager()

    class Meta:
        unique_together = ('tenant', 'sms_id')
        ordering = ['order']

    def __str__(self):
        return f"[{self.tenant.name}] {self.name}"


class CachedAlbum(models.Model):
    """
    Photo / video galleries.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    sms_id = models.CharField(max_length=50, db_index=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='albums/covers/', blank=True, null=True)
    media_items = models.JSONField(default=list, blank=True)  # Legacy/external URLs
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    last_synced = models.DateTimeField(auto_now=True)

    objects = TenantAwareManager()

    @property
    def total_media_count(self):
        """Returns the total count of both legacy URL media and local media items"""
        legacy_count = len(self.media_items) if self.media_items else 0
        local_count = self.local_media.count()
        return legacy_count + local_count

    def __str__(self):
        return f"[{self.tenant.name}] {self.title}"


class AlbumMedia(models.Model):
    """
    Individual media items (images/videos) within an album.
    """
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    
    album = models.ForeignKey(CachedAlbum, on_delete=models.CASCADE, related_name='local_media', null=True, blank=True)
    file = models.FileField(upload_to='albums/media/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    caption = models.CharField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        album_title = self.album.title if self.album else "Unassigned"
        return f"{self.media_type} for {album_title}"