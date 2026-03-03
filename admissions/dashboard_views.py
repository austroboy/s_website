from django.http import FileResponse
from django.utils.text import slugify
import os
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from dashboard.views import build_nav_context        # reuse sidebar nav

from .models import AdmissionForm


@login_required
def admission_form_list(request):
    tenant = request.tenant
    forms = AdmissionForm.objects.filter(tenant=tenant)

    edit_obj = None

    if request.method == "POST":
        action = request.POST.get("action")

        # CREATE
        if action == "create":
            AdmissionForm.objects.create(
                tenant=tenant,
                title=request.POST.get("title", "").strip(),
                description=request.POST.get("description", "").strip(),
                file=request.FILES.get("file"),
                order=int(request.POST.get("order") or 0),
                is_published="is_published" in request.POST,
            )
            messages.success(request, "Admission form created.")
            return redirect("admissions:admission_form_list")

        # UPDATE
        elif action == "update":
            pk = request.POST.get("form_id")
            form_obj = get_object_or_404(AdmissionForm, pk=pk, tenant=tenant)

            form_obj.title = request.POST.get("title", "").strip()
            form_obj.description = request.POST.get("description", "").strip()
            form_obj.order = int(request.POST.get("order") or 0)
            form_obj.is_published = "is_published" in request.POST

            if request.FILES.get("file"):
                form_obj.file = request.FILES.get("file")

            form_obj.save()
            messages.success(request, "Admission form updated.")
            return redirect("admissions:admission_form_list")

        # DELETE
        elif action == "delete":
            pk = request.POST.get("form_id")
            form_obj = get_object_or_404(AdmissionForm, pk=pk, tenant=tenant)
            form_obj.delete()
            messages.success(request, "Admission form deleted.")
            return redirect("admissions:admission_form_list")

        # TOGGLE
        elif action == "toggle":
            pk = request.POST.get("form_id")
            form_obj = get_object_or_404(AdmissionForm, pk=pk, tenant=tenant)
            form_obj.is_published = not form_obj.is_published
            form_obj.save()
            return redirect("admissions:admission_form_list")

    # Edit Mode
    edit_id = request.GET.get("edit")
    if edit_id:
        edit_obj = get_object_or_404(AdmissionForm, pk=edit_id, tenant=tenant)

    context = {
        "forms": forms,
        "edit_obj": edit_obj,
        **build_nav_context(request),
    }

    return render(request, "dashboard/admission/admission_form_list.html", context)


@login_required
def admission_form_download(request, pk):
    tenant = request.tenant
    form_obj = get_object_or_404(AdmissionForm, pk=pk, tenant=tenant)

    response = FileResponse(form_obj.file.open(), as_attachment=True)
    response["Content-Disposition"] = f'attachment; filename="{os.path.basename(form_obj.file.name)}"'
    return response