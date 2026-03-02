"""
branding/urls.py

Include in your project urls.py as:
    path('settings/branding/', include('branding.urls', namespace='branding')),
"""
from django.urls import path
from .views import (
    colors_list,
    colors_create,
    colors_update,
    colors_delete,
)

app_name = 'branding'

urlpatterns = [
    # GET  /settings/branding/colors/         — list or empty state
    path('settings/branding/colors/',         colors_list,   name='colors-list'),

    # GET  /settings/branding/colors/create/  — create form
    # POST /settings/branding/colors/create/  — save new palette
    path('colors/create/',  colors_create, name='colors-create'),

    # GET  /settings/branding/colors/update/  — prefilled edit form
    # POST /settings/branding/colors/update/  — save changes
    path('colors/update/',  colors_update, name='colors-update'),

    # POST /settings/branding/colors/delete/  — delete (form submit from modal)
    path('colors/delete/',  colors_delete, name='colors-delete'),
]
