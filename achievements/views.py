from django.views.generic import ListView, DetailView
from .models import Achievement

class AchievementListView(ListView):
    model = Achievement
    template_name = 'components/page/list/achievements.html'
    context_object_name = 'achievements'
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().filter(tenant=self.request.tenant, is_published=True)

class AchievementDetailView(DetailView):
    model = Achievement
    template_name = 'components/page/details/achievement.html'
    context_object_name = 'achievement'

    def get_queryset(self):
        return super().get_queryset().filter(tenant=self.request.tenant, is_published=True)