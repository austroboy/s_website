from django.contrib import admin
from .models import Tenant, Domain


class DomainInline(admin.TabularInline):
    model = Domain
    extra = 0
    fields = ("domain", "is_primary", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("-is_primary", "domain")


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sms_tenant_id",
        "subdomain",
        "api_base_url",
        "enable_news",
        "enable_events",
        "enable_notices",
        "enable_staff_directory",
        "enable_gallery",
        "enable_admissions",
        "enable_results",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "enable_news",
        "enable_events",
        "enable_notices",
        "enable_staff_directory",
        "enable_gallery",
        "enable_admissions",
        "enable_results",
        "created_at",
    )
    search_fields = ("name", "sms_tenant_id", "subdomain", "contact_email", "contact_phone")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Tenant Identity", {"fields": ("name", "sms_tenant_id", "subdomain")}),
        ("SMS API Credentials", {"fields": ("api_base_url", "api_key", "api_secret")}),
        ("Feature Flags", {
            "fields": (
                "enable_news",
                "enable_events",
                "enable_notices",
                "enable_staff_directory",
                "enable_gallery",
                "enable_admissions",
                "enable_results",
            )
        }),
        ("Contact Info", {"fields": ("contact_email", "contact_phone", "address")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    inlines = [DomainInline]


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("domain", "tenant", "is_primary", "created_at")
    list_filter = ("is_primary", "created_at")
    search_fields = ("domain", "tenant__name", "tenant__sms_tenant_id")
    autocomplete_fields = ("tenant",)
    ordering = ("-is_primary", "domain")
    readonly_fields = ("created_at",)
