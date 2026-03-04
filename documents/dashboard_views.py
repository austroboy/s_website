from django.utils.text import slugify
from .models import DocumentCategory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from dashboard.views import build_nav_context        # reuse sidebar nav
from django.http import FileResponse
import os
from .models import Document, DocumentCategory



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







@login_required
def document_list(request):
    tenant = request.tenant
    documents = Document.objects.filter(tenant=tenant).select_related("category")
    categories = DocumentCategory.objects.filter(tenant=tenant)

    edit_obj = None

    if request.method == "POST":
        action = request.POST.get("action")

        # CREATE
        if action == "create":
            Document.objects.create(
                tenant=tenant,
                category_id=request.POST.get("category") or None,
                title=request.POST.get("title", "").strip(),
                description=request.POST.get("description", "").strip(),
                file=request.FILES.get("file"),
                order=int(request.POST.get("order") or 0),
                is_published="is_published" in request.POST,
            )
            messages.success(request, "Document created.")
            return redirect("documents:document_list")

        # UPDATE
        elif action == "update":
            pk = request.POST.get("document_id")
            doc = get_object_or_404(Document, pk=pk, tenant=tenant)

            doc.category_id = request.POST.get("category") or None
            doc.title = request.POST.get("title", "").strip()
            doc.description = request.POST.get("description", "").strip()
            doc.order = int(request.POST.get("order") or 0)
            doc.is_published = "is_published" in request.POST

            if request.FILES.get("file"):
                doc.file = request.FILES.get("file")

            doc.save()
            messages.success(request, "Document updated.")
            return redirect("documents:document_list")

        # DELETE
        elif action == "delete":
            pk = request.POST.get("document_id")
            doc = get_object_or_404(Document, pk=pk, tenant=tenant)
            doc.delete()
            messages.success(request, "Document deleted.")
            return redirect("documents:document_list")

        # TOGGLE
        elif action == "toggle":
            pk = request.POST.get("document_id")
            doc = get_object_or_404(Document, pk=pk, tenant=tenant)
            doc.is_published = not doc.is_published
            doc.save()
            return redirect("documents:document_list")

    # EDIT MODE
    edit_id = request.GET.get("edit")
    if edit_id:
        edit_obj = get_object_or_404(Document, pk=edit_id, tenant=tenant)

    context = {
        "documents": documents,
        "categories": categories,
        "edit_obj": edit_obj,
        **build_nav_context(request),
    }

    return render(request, "dashboard/documents/document_list.html", context)


@login_required
def document_download(request, pk):
    tenant = request.tenant
    doc = get_object_or_404(Document, pk=pk, tenant=tenant)

    response = FileResponse(doc.file.open(), as_attachment=True)
    response["Content-Disposition"] = f'attachment; filename="{os.path.basename(doc.file.name)}"'
    return response