from django.contrib import admin
from .models import (
    CachedNews,
    CachedEvent,
    CachedNotice,
    CachedStaff,
    CachedProgram,
    CachedAlbum,
)


# =========================
# Shared helpers / mixins
# =========================
class TenantFilterMixin:
    """Common admin config for tenant-based cached models."""
    search_fields = ("tenant__name", "tenant__tenant_key", "sms_id", "title", "slug")
    list_filter = ("tenant", "is_published")
    ordering = ("-last_synced",)
    date_hierarchy = "last_synced"


class BaseCachedAdmin(admin.ModelAdmin, TenantFilterMixin):
    list_display = (
        "tenant",
        "title",
        "sms_id",
        "is_published",
        "created_at",
        "updated_at",
        "last_synced",
    )
    list_select_related = ("tenant",)

    fieldsets = (
        ("Tenant & Sync", {
            "fields": ("tenant", "sms_id", "is_published", "last_synced"),
        }),
        ("Content", {
            "fields": (
                "title",
                "slug",
                "summary",
                "content",
                "featured_image",
            )
        }),
        ("Timestamps (from SMS)", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    readonly_fields = ("last_synced",)


# =========================
# News
# =========================
@admin.register(CachedNews)
class CachedNewsAdmin(BaseCachedAdmin):
    list_display = (
        "tenant",
        "title",
        "category",
        "author_name",
        "sms_id",
        "is_published",
        "updated_at",
        "last_synced",
    )

    search_fields = BaseCachedAdmin.search_fields + ("author_name", "category")
    list_filter = ("tenant", "is_published", "category")
    fieldsets = BaseCachedAdmin.fieldsets + (
        ("News Meta", {"fields": ("author_name", "category", "tags")}),
    )


# =========================
# Event
# =========================
@admin.register(CachedEvent)
class CachedEventAdmin(BaseCachedAdmin):
    list_display = (
        "tenant",
        "title",
        "start_date",
        "end_date",
        "venue",
        "sms_id",
        "is_published",
        "last_synced",
    )

    search_fields = BaseCachedAdmin.search_fields + ("venue",)
    list_filter = ("tenant", "is_published", "start_date")
    fieldsets = BaseCachedAdmin.fieldsets + (
        ("Event Details", {"fields": ("start_date", "end_date", "venue", "registration_link")}),
    )


# =========================
# Notice
# =========================
@admin.register(CachedNotice)
class CachedNoticeAdmin(BaseCachedAdmin):
    list_display = (
        "tenant",
        "title",
        "expiry_date",
        "sms_id",
        "is_published",
        "updated_at",
        "last_synced",
    )

    fieldsets = BaseCachedAdmin.fieldsets + (
        ("Notice Details", {"fields": ("expiry_date", "attachment_url")}),
    )


# =========================
# Staff
# =========================
@admin.register(CachedStaff)
class CachedStaffAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "name",
        "designation",
        "department",
        "order",
        "is_published",
        "sms_id",
        "last_synced",
    )
    list_select_related = ("tenant",)
    list_filter = ("tenant", "is_published", "department")
    search_fields = ("tenant__name", "tenant__tenant_key", "sms_id", "name", "designation", "department", "email", "phone")
    ordering = ("tenant", "order", "name")
    readonly_fields = ("last_synced",)

    fieldsets = (
        ("Tenant & Sync", {"fields": ("tenant", "sms_id", "is_published", "last_synced")}),
        ("Profile", {"fields": ("name", "designation", "department", "bio", "photo")}),
        ("Contact", {"fields": ("email", "phone")}),
        ("Display", {"fields": ("order",)}),
    )


# =========================
# Program
# =========================
@admin.register(CachedProgram)
class CachedProgramAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "name",
        "order",
        "is_published",
        "sms_id",
        "last_synced",
    )
    list_select_related = ("tenant",)
    list_filter = ("tenant", "is_published")
    search_fields = ("tenant__name", "tenant__tenant_key", "sms_id", "name")
    ordering = ("tenant", "order", "name")
    readonly_fields = ("last_synced",)

    fieldsets = (
        ("Tenant & Sync", {"fields": ("tenant", "sms_id", "is_published", "last_synced")}),
        ("Program", {"fields": ("name", "description", "icon")}),
        ("Display", {"fields": ("order",)}),
    )


# =========================
# Album / Gallery
# =========================
@admin.register(CachedAlbum)
class CachedAlbumAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "title",
        "sms_id",
        "is_published",
        "created_at",
        "last_synced",
    )
    list_select_related = ("tenant",)
    list_filter = ("tenant", "is_published")
    search_fields = ("tenant__name", "tenant__tenant_key", "sms_id", "title")
    ordering = ("-created_at", "-last_synced")
    readonly_fields = ("last_synced",)

    fieldsets = (
        ("Tenant & Sync", {"fields": ("tenant", "sms_id", "is_published", "last_synced")}),
        ("Album", {"fields": ("title", "description", "cover_image", "media_items")}),
        ("Timestamps (from SMS)", {"fields": ("created_at",)}),
    )
