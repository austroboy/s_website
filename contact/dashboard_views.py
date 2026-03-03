from .models import AdmissionInquiry,ContactSubmission
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from dashboard.views import build_nav_context        # reuse sidebar nav


@login_required
def admission_inquiry_list(request):
    tenant = request.tenant
    inquiries = AdmissionInquiry.objects.filter(
        tenant=tenant
    ).order_by("-created_at")

    context = {
        "inquiries": inquiries,
        "tenant": tenant,
        **build_nav_context(request),
    }

    return render(
        request,
        "dashboard/admission_inquiry/admission_inquiry_list.html",
        context,
    )


@login_required
@require_POST
def admission_inquiry_toggle(request, pk):
    inquiry = get_object_or_404(
        AdmissionInquiry,
        pk=pk,
        tenant=request.tenant,
    )

    inquiry.is_contacted = not inquiry.is_contacted
    inquiry.save(update_fields=["is_contacted"])

    messages.success(request, "Inquiry status updated.")
    return redirect("contact:admission_inquiry_list")






@login_required
def contact_submission_list(request):
    tenant = request.tenant

    submissions = ContactSubmission.objects.filter(
        tenant=tenant
    ).order_by("-created_at")

    context = {
        "submissions": submissions,
        "tenant": tenant,
        **build_nav_context(request),
    }

    return render(
        request,
        "dashboard/contact/contact_submission_list.html",
        context,
    )


@login_required
@require_POST
def contact_submission_toggle(request, pk):
    submission = get_object_or_404(
        ContactSubmission,
        pk=pk,
        tenant=request.tenant,
    )

    submission.is_read = not submission.is_read
    submission.save(update_fields=["is_read"])

    messages.success(request, "Message status updated.")
    return redirect("contact:contact_submission_list")