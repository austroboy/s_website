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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import *



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




def _base_ctx(request):
    
    return {'tenant': request.tenant, **build_nav_context(request)}


def _form_ctx(form, font_pair=None):
    """
    Extra context needed to render the template:
      weight_choices          — list of (value, label) for all weight chips
      selected_heading_weights — set of currently selected heading weight strings
      selected_body_weights    — set of currently selected body weight strings
    """
    hw_raw = form['heading_weights'].value() or '400,600,700'
    bw_raw = form['body_weights'].value()    or '400,500'
    return {
        'weight_choices':         WEIGHT_CHOICES,
        'selected_heading_weights': set(hw_raw.split(',')),
        'selected_body_weights':    set(bw_raw.split(',')),
    }


@login_required
def fonts_list(request):
    """List page — shows specimen if FontPair exists, else empty state."""
    font_pair = FontPair.objects.filter(tenant=request.tenant).first()

    # Attach helper property for template weight iteration
 
    return render(request, 'branding/fonts/list.html', {
        **_base_ctx(request),
        'font_pair': font_pair,
    })


@login_required
def fonts_create(request):
    if FontPair.objects.filter(tenant=request.tenant).exists():
        return redirect('branding:fonts-update')

    if request.method == 'POST':
        form = FontPairForm(request.POST)
        if form.is_valid():
            fp = form.save(commit=False)
            fp.tenant = request.tenant
            fp.save()
            messages.success(request, 'Font pair created successfully.')
            return redirect('branding:fonts-list')
    else:
        form = FontPairForm()

    return render(request, 'branding/fonts/form.html', {
        **_base_ctx(request),
        'form': form,
        **_form_ctx(form),
    })


@login_required
def fonts_update(request):
    font_pair = get_object_or_404(FontPair, tenant=request.tenant)

    if request.method == 'POST':
        form = FontPairForm(request.POST, instance=font_pair)
        if form.is_valid():
            form.save()
            messages.success(request, 'Font pair updated successfully.')
            return redirect('branding:fonts-list')
    else:
        form = FontPairForm(instance=font_pair)

    return render(request, 'branding/fonts/form.html', {
        **_base_ctx(request),
        'form':      form,
        'font_pair': font_pair,
        **_form_ctx(form, font_pair),
    })


@login_required
@require_POST
def fonts_delete(request):
    font_pair = get_object_or_404(FontPair, tenant=request.tenant)
    font_pair.delete()
    messages.success(request, 'Font pair deleted. Website will use system fonts.')
    return redirect('branding:fonts-list')
