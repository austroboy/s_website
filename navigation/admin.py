from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    fields = ("title", "parent", "page", "url", "order", "target_blank", "is_active")
    autocomplete_fields = ("parent", "page")
    ordering = ("order",)
    show_change_link = True


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("tenant", "name", "slug", "created_at")
    list_filter = ("tenant", "created_at")
    search_fields = ("tenant__name", "tenant__tenant_key", "name", "slug")
    ordering = ("tenant", "name")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)

    inlines = (MenuItemInline,)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "menu",
        "title",
        "parent",
        "order",
        "is_active",
        "target_blank",
        "page",
        "url",
    )
    list_filter = ("menu__tenant", "menu", "is_active", "target_blank")
    search_fields = (
        "menu__tenant__name",
        "menu__tenant__tenant_key",
        "menu__name",
        "menu__slug",
        "title",
        "url",
        "page__title",
        "page__slug",
    )
    ordering = ("menu", "parent__id", "order", "title")
    list_select_related = ("menu", "menu__tenant", "parent", "page")
    list_editable = ("order", "is_active")

    autocomplete_fields = ("menu", "parent", "page")

    fieldsets = (
        ("Menu", {"fields": ("menu", "parent", "order", "is_active")}),
        ("Label", {"fields": ("title",)}),
        ("Link", {"fields": ("page", "url", "target_blank")}),
    )
