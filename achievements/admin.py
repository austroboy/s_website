from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Achievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "title",
        "date",
        "order",
        "is_published",
        "image_thumb",
        "updated_at",
    )
    list_filter = ("tenant", "is_published", "date")
    search_fields = ("tenant__name", "tenant__tenant_key", "title", "description")
    ordering = ("tenant", "order", "-date")
    list_editable = ("order", "is_published")
    readonly_fields = ("created_at", "updated_at", "image_preview")
    date_hierarchy = "date"

    fieldsets = (
        ("Tenant", {"fields": ("tenant",)}),
        ("Achievement", {"fields": ("title", "description", "date")}),
        ("Image", {"fields": ("image", "image_preview")}),
        ("Publish & Order", {"fields": ("is_published", "order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def image_thumb(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="height:28px;width:auto;border-radius:6px;" />'
            )
        return "—"
    image_thumb.short_description = "Image"

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height:220px;width:auto;border-radius:10px;" />'
            )
        return "—"
    image_preview.short_description = "Preview"
