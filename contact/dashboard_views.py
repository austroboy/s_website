from .models import AdmissionInquiry
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