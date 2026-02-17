from django.contrib import admin
from .models import DocumentCategory, Document


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    fields = ("title", "category", "order", "is_published", "updated_at")
    readonly_fields = ("updated_at",)
    show_change_link = True
    ordering = ("order",)


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("tenant", "name", "slug", "order")
    list_filter = ("tenant",)
    search_fields = ("tenant__name", "tenant__tenant_key", "name", "slug")
    ordering = ("tenant", "order", "name")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}

    inlines = (DocumentInline,)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "title",
        "category",
        "order",
        "is_published",
        "created_at",
        "updated_at",
    )
    list_filter = ("tenant", "category", "is_published", "created_at", "updated_at")
    search_fields = (
        "tenant__name",
        "tenant__tenant_key",
        "title",
        "description",
        "category__name",
        "category__slug",
    )
    ordering = ("tenant", "order", "title")
    list_editable = ("order", "is_published")
    list_select_related = ("tenant", "category")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Tenant & Category", {"fields": ("tenant", "category")}),
        ("Document Info", {"fields": ("title", "description")}),
        ("File", {"fields": ("file",)}),
        ("Publish & Order", {"fields": ("is_published", "order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
