"""
branding/urls.py

Include in your project urls.py as:
    path('settings/branding/', include('branding.urls', namespace='branding')),
"""
from django.urls import path
from .views import *

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

    path('fonts/',         fonts_list,   name='fonts-list'),
    path('fonts/create/',  fonts_create, name='fonts-create'),
    path('fonts/update/',  fonts_update, name='fonts-update'),
    path('fonts/delete/',  fonts_delete, name='fonts-delete'),

       # ── Brand Assets ────────────────────────────────────────────────
    path(
        'settings/branding/assets/',
        brand_assets_view,
        name='brand_assets',
    ),
    path(
        'settings/branding/assets/delete/',
        brand_assets_delete,
        name='brand_assets_delete',
    ),
]
