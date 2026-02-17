from django.contrib import admin
from .models import Page, HomepageSection


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "title",
        "slug",
        "published",
        "show_in_footer",
        "updated_at",
    )
    list_filter = ("tenant", "published", "show_in_footer", "updated_at")
    search_fields = ("tenant__name", "tenant__tenant_key", "title", "slug", "meta_description", "content")
    ordering = ("tenant", "title")
    date_hierarchy = "updated_at"
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Tenant", {"fields": ("tenant",)}),
        ("Page Content", {"fields": ("title", "slug", "content")}),
        ("SEO", {"fields": ("meta_description",)}),
        ("Publish Settings", {"fields": ("published", "show_in_footer")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(HomepageSection)
class HomepageSectionAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "section_type",
        "title",
        "order",
        "is_active",
    )
    list_filter = ("tenant", "section_type", "is_active")
    search_fields = ("tenant__name", "tenant__tenant_key", "title", "subtitle")
    ordering = ("tenant", "order")
    list_editable = ("order", "is_active")
    list_select_related = ("tenant",)

    fieldsets = (
        ("Tenant", {"fields": ("tenant",)}),
        ("Section", {"fields": ("section_type", "title", "subtitle")}),
        ("Behavior", {"fields": ("order", "is_active")}),
        ("Config (JSON)", {"fields": ("config",)}),
    )
