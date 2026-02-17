from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import ColorPalette, FontPair, BrandAssets


@admin.register(ColorPalette)
class ColorPaletteAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "primary",
        "secondary",
        "accent",
        "surface",
        "text",
        "success",
        "warning",
        "error",
    )
    search_fields = ("tenant__name", "tenant__tenant_key")

    fieldsets = (
        ("Tenant", {"fields": ("tenant",)}),
        ("Light Mode Colors", {
            "fields": (
                "primary", "secondary", "accent",
                "surface", "text", "text_muted",
                "success", "warning", "error",
            )
        }),
        ("Dark Mode Overrides (Optional)", {
            "fields": ("dark_primary", "dark_surface", "dark_text"),
            "classes": ("collapse",),
        }),
    )


@admin.register(FontPair)
class FontPairAdmin(admin.ModelAdmin):
    list_display = ("tenant", "heading_font", "body_font", "heading_weights", "body_weights")
    search_fields = ("tenant__name", "tenant__tenant_key")

    fieldsets = (
        ("Tenant", {"fields": ("tenant",)}),
        ("Heading Font", {"fields": ("heading_font", "heading_weights")}),
        ("Body Font", {"fields": ("body_font", "body_weights")}),
    )


@admin.register(BrandAssets)
class BrandAssetsAdmin(admin.ModelAdmin):
    list_display = ("tenant", "logo_light_thumb", "favicon_thumb")
    search_fields = ("tenant__name", "tenant__tenant_key")

    readonly_fields = (
        "logo_light_thumb_big",
        "logo_dark_thumb_big",
        "favicon_thumb_big",
        "og_thumb_big",
        "footer_logo_thumb_big",
    )

    fieldsets = (
        ("Tenant", {"fields": ("tenant",)}),
        ("Logos", {
            "fields": (
                "logo_light", "logo_light_thumb_big",
                "logo_dark", "logo_dark_thumb_big",
                "footer_logo", "footer_logo_thumb_big",
            )
        }),
        ("Icons & Social", {
            "fields": (
                "favicon", "favicon_thumb_big",
                "og_image", "og_thumb_big",
            )
        }),
    )

    # ---------- Helpers ----------
    def _thumb(self, obj, field, height=40):
        f = getattr(obj, field)
        if f:
            return mark_safe(f'<img src="{f.url}" style="height:{height}px; width:auto; border-radius:6px;" />')
        return "—"

    # list_display thumbs
    def logo_light_thumb(self, obj):
        return self._thumb(obj, "logo_light", height=28)
    logo_light_thumb.short_description = "Logo (Light)"

    def favicon_thumb(self, obj):
        return self._thumb(obj, "favicon", height=22)
    favicon_thumb.short_description = "Favicon"

    # detail page bigger previews (readonly_fields)
    def logo_light_thumb_big(self, obj):
        return self._thumb(obj, "logo_light", height=80)
    logo_light_thumb_big.short_description = "Preview"

    def logo_dark_thumb_big(self, obj):
        return self._thumb(obj, "logo_dark", height=80)
    logo_dark_thumb_big.short_description = "Preview"

    def favicon_thumb_big(self, obj):
        return self._thumb(obj, "favicon", height=48)
    favicon_thumb_big.short_description = "Preview"

    def og_thumb_big(self, obj):
        return self._thumb(obj, "og_image", height=80)
    og_thumb_big.short_description = "Preview"

    def footer_logo_thumb_big(self, obj):
        return self._thumb(obj, "footer_logo", height=80)
    footer_logo_thumb_big.short_description = "Preview"
