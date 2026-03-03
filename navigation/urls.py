from django.urls import path
from .import dashboard_views
app_name = 'navigation'

urlpatterns = [
path("menus/", dashboard_views.menu_list, name="menu_list"),
path("menus/<int:menu_id>/items/",
     dashboard_views.menu_item_manager,
     name="menu_item_manager"),
]