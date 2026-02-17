from django.contrib import admin
from .models import ContactSubmission, AdmissionInquiry


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "name",
        "email",
        "phone",
        "subject",
        "is_read",
        "created_at",
    )
    list_filter = ("tenant", "is_read", "created_at")
    search_fields = ("tenant__name", "tenant__tenant_key", "name", "email", "phone", "subject", "message", "ip_address")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    readonly_fields = ("created_at", "ip_address")

    fieldsets = (
        ("Tenant", {"fields": ("tenant",)}),
        ("Sender", {"fields": ("name", "email", "phone")}),
        ("Message", {"fields": ("subject", "message")}),
        ("Meta", {"fields": ("is_read", "ip_address", "created_at")}),
    )

    actions = ("mark_as_read", "mark_as_unread")

    @admin.action(description="Mark selected as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)


@admin.register(AdmissionInquiry)
class AdmissionInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "full_name",
        "email",
        "phone",
        "program_of_interest",
        "grade_level",
        "is_contacted",
        "created_at",
    )
    list_filter = ("tenant", "is_contacted", "created_at", "program_of_interest", "grade_level")
    search_fields = (
        "tenant__name",
        "tenant__tenant_key",
        "full_name",
        "email",
        "phone",
        "program_of_interest",
        "grade_level",
        "message",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Tenant", {"fields": ("tenant",)}),
        ("Applicant", {"fields": ("full_name", "email", "phone")}),
        ("Interest", {"fields": ("program_of_interest", "grade_level")}),
        ("Message", {"fields": ("message",)}),
        ("Status", {"fields": ("is_contacted", "created_at")}),
    )

    actions = ("mark_as_contacted", "mark_as_not_contacted")

    @admin.action(description="Mark selected as contacted")
    def mark_as_contacted(self, request, queryset):
        queryset.update(is_contacted=True)

    @admin.action(description="Mark selected as not contacted")
    def mark_as_not_contacted(self, request, queryset):
        queryset.update(is_contacted=False)
