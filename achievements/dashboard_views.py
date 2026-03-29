from .models import Achievement
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from dashboard.views import build_nav_context        # reuse sidebar nav


@login_required
def achievement_manager(request):
    tenant = request.tenant
    achievements = Achievement.objects.filter(tenant=tenant)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            achievement = Achievement.objects.create(
                tenant=tenant,
                title=request.POST.get("title", "").strip(),
                description=request.POST.get("description", "").strip(),
                date=request.POST.get("date") or None,
                order=int(request.POST.get("order") or 0),
                is_published="is_published" in request.POST,
            )
            if request.FILES.get("image"):
                achievement.image = request.FILES["image"]
                achievement.save()
            messages.success(request, "Achievement created successfully.")
            return redirect("achievements:achievement_manager")

        elif action == "update":
            pk = request.POST.get("achievement_id")
            achievement = get_object_or_404(
                Achievement, pk=pk, tenant=tenant
            )

            achievement.title = request.POST.get("title", "").strip()
            achievement.description = request.POST.get("description", "").strip()
            achievement.date = request.POST.get("date") or None
            achievement.order = int(request.POST.get("order") or 0)
            achievement.is_published = "is_published" in request.POST
            if request.FILES.get("image"):
                achievement.image = request.FILES["image"]
            achievement.save()

            messages.success(request, "Achievement updated successfully.")
            return redirect("achievements:achievement_manager")

    context = {
        "achievements": achievements,
        "tenant": tenant,
        **build_nav_context(request),
    }
    return render(request, "dashboard/achivement/achievement_manager.html", context)


@login_required
@require_POST
def achievement_delete(request, pk):
    achievement = get_object_or_404(
        Achievement, pk=pk, tenant=request.tenant
    )
    achievement.delete()
    messages.success(request, "Achievement deleted.")
    return redirect("achievements:achievement_manager")