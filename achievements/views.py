from django.views.generic import ListView, DetailView
from .models import Achievement

class AchievementListView(ListView):
    model = Achievement
    template_name = 'achievements/list.html'
    context_object_name = 'achievements'
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().filter(tenant=self.request.tenant, is_published=True)

class AchievementDetailView(DetailView):
    model = Achievement
    template_name = 'achievements/detail.html'
    context_object_name = 'achievement'

    def get_queryset(self):
        return super().get_queryset().filter(tenant=self.request.tenant, is_published=True)