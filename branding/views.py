"""
branding/views/colors.py

CRUD views for the ColorPalette model.
URL names used:
    branding:colors-list
    branding:colors-create
    branding:colors-update
    branding:colors-delete
"""
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from dashboard.views import build_nav_context
from .models import ColorPalette


# ──────────────────────────────────────────────────────────
#  Form
# ──────────────────────────────────────────────────────────

class ColorPaletteForm(forms.ModelForm):
    """
    Exposes all ColorPalette fields.
    dark_* fields are optional (blank=True on the model).
    """

    class Meta:
        model  = ColorPalette
        # Exclude tenant — that's set in the view from request.tenant
        exclude = ['tenant']
        widgets = {
            # Every hex field gets a plain text input in the template.
            # The template renders a custom color-picker chip alongside it.
            f: forms.TextInput(attrs={
                'placeholder': '#000000',
                'maxlength': 7,
                'class': 'hex-input',
                'autocomplete': 'off',
            })
            for f in [
                'primary', 'primary_dark', 'primary_light',
                'secondary', 'secondary_light', 'accent',
                'surface', 'surface_alt', 'text', 'text_muted',
                'footer_bg', 'footer_text', 'border',
                'success', 'warning', 'error',
                'dark_primary', 'dark_surface', 'dark_text',
            ]
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # primary_glow allows rgba() strings, so use a wider text input
        self.fields['primary_glow'].widget = forms.TextInput(attrs={
            'placeholder': 'rgba(0, 81, 255, 0.35)',
            'class': 'hex-input',
        })
        # dark_* are optional
        for f in ['dark_primary', 'dark_surface', 'dark_text']:
            self.fields[f].required = False

    def clean(self):
        """Validate that all hex fields are valid 7-char hex strings."""
        cleaned = super().clean()
        hex_fields = [
            'primary', 'primary_dark', 'primary_light',
            'secondary', 'secondary_light', 'accent',
            'surface', 'surface_alt', 'text', 'text_muted',
            'footer_bg', 'footer_text', 'border',
            'success', 'warning', 'error',
            'dark_primary', 'dark_surface', 'dark_text',
        ]
        import re
        hex_re = re.compile(r'^#[0-9A-Fa-f]{6}$')
        for field_name in hex_fields:
            val = cleaned.get(field_name, '')
            if val and not hex_re.match(val):
                self.add_error(field_name, 'Enter a valid hex color (e.g. #0051FF)')
        return cleaned


# ──────────────────────────────────────────────────────────
#  Shared context helper
# ──────────────────────────────────────────────────────────

def _base_context(request):
    """Returns nav context for the sidebar — same as dashboard."""
    return {'tenant': request.tenant, **build_nav_context(request)}


# ──────────────────────────────────────────────────────────
#  List / overview view
# ──────────────────────────────────────────────────────────

@login_required
def colors_list(request):
    """
    Show the existing ColorPalette for this tenant.
    If none exists, show empty state with 'Create' CTA.
    """
    palette = ColorPalette.objects.filter(tenant=request.tenant).first()

    return render(request, 'branding/colors/list.html', {
        **_base_context(request),
        'palette': palette,
    })


# ──────────────────────────────────────────────────────────
#  Create view
# ──────────────────────────────────────────────────────────

@login_required
def colors_create(request):
    """
    Create a new ColorPalette for this tenant.
    Redirect to list if one already exists (use update instead).
    """
    # Guard: redirect to update if palette already exists
    if ColorPalette.objects.filter(tenant=request.tenant).exists():
        return redirect('branding:colors-update')

    if request.method == 'POST':
        form = ColorPaletteForm(request.POST)
        if form.is_valid():
            palette = form.save(commit=False)
            palette.tenant = request.tenant
            palette.save()
            messages.success(request, 'Color palette created successfully.')
            return redirect('branding:colors-list')
    else:
        form = ColorPaletteForm()

    return render(request, 'branding/colors/form.html', {
        **_base_context(request),
        'form': form,
        'mode': 'create',
    })


# ──────────────────────────────────────────────────────────
#  Update view
# ──────────────────────────────────────────────────────────

@login_required
def colors_update(request):
    """
    Update the existing ColorPalette for this tenant.
    Uses get_object_or_404 — if none exists, 404 (frontend should show Create instead).
    """
    palette = get_object_or_404(ColorPalette, tenant=request.tenant)

    if request.method == 'POST':
        form = ColorPaletteForm(request.POST, instance=palette)
        if form.is_valid():
            form.save()
            messages.success(request, 'Color palette updated successfully.')
            return redirect('branding:colors-list')
    else:
        form = ColorPaletteForm(instance=palette)

    return render(request, 'branding/colors/form.html', {
        **_base_context(request),
        'form': form,
        'mode': 'update',
        'palette': palette,
    })


# ──────────────────────────────────────────────────────────
#  Delete view  (POST only)
# ──────────────────────────────────────────────────────────

@login_required
@require_POST
def colors_delete(request):
    """
    Hard-delete the ColorPalette for this tenant.
    Only accepts POST (CSRF-protected form submission from the modal).
    """
    palette = get_object_or_404(ColorPalette, tenant=request.tenant)
    palette.delete()
    messages.success(request, 'Color palette deleted. Website will use default colors.')
    return redirect('branding:colors-list')