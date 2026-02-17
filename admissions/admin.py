from django.contrib import admin
from .models import AdmissionForm


@admin.register(AdmissionForm)
class AdmissionFormAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "title",
        "order",
        "is_published",
        "created_at",
        "updated_at",
    )
    list_filter = ("tenant", "is_published", "created_at", "updated_at")
    search_fields = ("tenant__name", "tenant__tenant_key", "title", "description")
    ordering = ("tenant", "order", "title")
    list_editable = ("order", "is_published")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Tenant", {"fields": ("tenant",)}),
        ("Form Info", {"fields": ("title", "description")}),
        ("File", {"fields": ("file",)}),
        ("Publish & Order", {"fields": ("order", "is_published")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
