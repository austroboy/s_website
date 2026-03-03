from .models import Menu, MenuItem
from content.models import Page  # adjust if needed
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from dashboard.views import build_nav_context        # reuse sidebar nav

@login_required
def menu_list(request):
    tenant = request.tenant
    menus = Menu.objects.filter(tenant=tenant)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            Menu.objects.create(
                tenant=tenant,
                name=request.POST.get("name", "").strip(),
                slug=request.POST.get("slug", "").strip(),
            )
            messages.success(request, "Menu created.")
            return redirect("navigation:menu_list")

        elif action == "update":
            pk = request.POST.get("menu_id")
            menu = get_object_or_404(Menu, pk=pk, tenant=tenant)
            menu.name = request.POST.get("name", "").strip()
            menu.slug = request.POST.get("slug", "").strip()
            menu.save()
            messages.success(request, "Menu updated.")
            return redirect("navigation:menu_list")

    context = {
        "menus": menus,
        "tenant": tenant,
        **build_nav_context(request),
    }

    return render(request, "dashboard/navigation/menu_list.html", context)



@login_required
def menu_item_manager(request, menu_id):
    tenant = request.tenant
    menu = get_object_or_404(Menu, pk=menu_id, tenant=tenant)

    items = MenuItem.objects.filter(menu=menu).select_related("parent", "page")
    pages = Page.objects.filter(tenant=tenant)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            MenuItem.objects.create(
                menu=menu,
                parent_id=request.POST.get("parent") or None,
                title=request.POST.get("title", "").strip(),
                url=request.POST.get("url", "").strip(),
                page_id=request.POST.get("page") or None,
                order=int(request.POST.get("order") or 0),
                target_blank="target_blank" in request.POST,
                is_active="is_active" in request.POST,
            )
            messages.success(request, "Menu item created.")
            return redirect("navigation:menu_item_manager", menu_id=menu.id)

        elif action == "update":
            pk = request.POST.get("item_id")
            item = get_object_or_404(MenuItem, pk=pk, menu=menu)

            item.parent_id = request.POST.get("parent") or None
            item.title = request.POST.get("title", "").strip()
            item.url = request.POST.get("url", "").strip()
            item.page_id = request.POST.get("page") or None
            item.order = int(request.POST.get("order") or 0)
            item.target_blank = "target_blank" in request.POST
            item.is_active = "is_active" in request.POST
            item.save()

            messages.success(request, "Menu item updated.")
            return redirect("navigation:menu_item_manager", menu_id=menu.id)
    context = {
        "menu": menu,
        "items": items,
        "pages": pages,
        **build_nav_context(request),
    }

    return render(request, "dashboard/navigation/menu_item_manager.html", context)
@login_required
def delete_menu_item_manager(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    menu_item.delete()
    messages.success(request, "Menu item deleted.")
    return redirect("navigation:menu_list")