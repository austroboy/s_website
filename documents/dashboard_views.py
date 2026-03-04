from django.utils.text import slugify
from .models import DocumentCategory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from dashboard.views import build_nav_context        # reuse sidebar nav



@login_required
def document_category_list(request):
    tenant = request.tenant
    categories = DocumentCategory.objects.filter(tenant=tenant)

    edit_obj = None

    if request.method == "POST":
        action = request.POST.get("action")

        # CREATE
        if action == "create":
            DocumentCategory.objects.create(
                tenant=tenant,
                name=request.POST.get("name", "").strip(),
                slug=slugify(request.POST.get("slug", "").strip()),
                order=int(request.POST.get("order") or 0),
            )
            messages.success(request, "Category created.")
            return redirect("documents:document_category_list")

        # UPDATE
        elif action == "update":
            pk = request.POST.get("category_id")
            category = get_object_or_404(DocumentCategory, pk=pk, tenant=tenant)

            category.name = request.POST.get("name", "").strip()
            category.slug = slugify(request.POST.get("slug", "").strip())
            category.order = int(request.POST.get("order") or 0)
            category.save()

            messages.success(request, "Category updated.")
            return redirect("documents:document_category_list")

        # DELETE
        elif action == "delete":
            pk = request.POST.get("category_id")
            category = get_object_or_404(DocumentCategory, pk=pk, tenant=tenant)
            category.delete()

            messages.success(request, "Category deleted.")
            return redirect("documents:document_category_list")

    # EDIT MODE
    edit_id = request.GET.get("edit")
    if edit_id:
        edit_obj = get_object_or_404(DocumentCategory, pk=edit_id, tenant=tenant)

    context = {
        "categories": categories,
        "edit_obj": edit_obj,
        **build_nav_context(request),
    }

    return render(request, "dashboard/documents/document_category_list.html", context)