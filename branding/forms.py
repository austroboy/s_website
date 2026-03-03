from django import forms
from .models import FontPair


# Curated Google Fonts grouped by category
GOOGLE_FONT_CHOICES = [
    ("Display", [
        ("Syne",                "Syne"),
        ("Playfair Display",    "Playfair Display"),
        ("Cormorant Garamond",  "Cormorant Garamond"),
        ("Fraunces",            "Fraunces"),
        ("Raleway",             "Raleway"),
        ("Josefin Sans",        "Josefin Sans"),
    ]),
    ("Serif", [
        ("Libre Baskerville",   "Libre Baskerville"),
        ("Merriweather",        "Merriweather"),
        ("Lora",                "Lora"),
        ("PT Serif",            "PT Serif"),
    ]),
    ("Sans-Serif", [
        ("DM Sans",             "DM Sans"),
        ("Inter",               "Inter"),
        ("Montserrat",          "Montserrat"),
        ("Poppins",             "Poppins"),
        ("Nunito",              "Nunito"),
        ("Lato",                "Lato"),
        ("Oswald",              "Oswald"),
        ("Space Grotesk",       "Space Grotesk"),
        ("Outfit",              "Outfit"),
        ("Plus Jakarta Sans",   "Plus Jakarta Sans"),
        ("Open Sans",           "Open Sans"),
        ("Source Sans 3",       "Source Sans 3"),
        ("Rubik",               "Rubik"),
        ("Mulish",              "Mulish"),
        ("Karla",               "Karla"),
        ("Work Sans",           "Work Sans"),
        ("Manrope",             "Manrope"),
        ("Noto Sans",           "Noto Sans"),
    ]),
    ("Monospace", [
        ("JetBrains Mono",      "JetBrains Mono"),
        ("Fira Code",           "Fira Code"),
    ]),
]

# All available weight values + human label pairs
WEIGHT_CHOICES = [
    ("100", "Thin"),
    ("200", "ExtraLight"),
    ("300", "Light"),
    ("400", "Regular"),
    ("500", "Medium"),
    ("600", "SemiBold"),
    ("700", "Bold"),
    ("800", "ExtraBold"),
    ("900", "Black"),
]


class FontPairForm(forms.ModelForm):
    """
    Form for FontPair model.
    heading_font / body_font — grouped select from curated Google Fonts list.
    heading_weights / body_weights — plain CharField; the template renders
      clickable weight chips that write a comma string into a hidden input.
    """

    heading_font = forms.ChoiceField(
        choices=GOOGLE_FONT_CHOICES,
        widget=forms.Select(attrs={'class': 'font-select'}),
    )
    body_font = forms.ChoiceField(
        choices=GOOGLE_FONT_CHOICES,
        widget=forms.Select(attrs={'class': 'font-select'}),
    )

    class Meta:
        model   = FontPair
        exclude = ['tenant']
        widgets = {
            'heading_weights': forms.HiddenInput(),
            'body_weights':    forms.HiddenInput(),
        }

    def clean_heading_weights(self):
        return self._clean_weights(self.cleaned_data.get('heading_weights', ''))

    def clean_body_weights(self):
        return self._clean_weights(self.cleaned_data.get('body_weights', ''))

    @staticmethod
    def _clean_weights(raw: str) -> str:
        """
        Normalise weights string:  "400,600,700"
        Strips whitespace, removes duplicates, validates each token.
        """
        valid = {w for w, _ in WEIGHT_CHOICES}
        parts = [p.strip() for p in raw.split(',') if p.strip()]
        clean = sorted(set(parts), key=lambda x: int(x))
        invalid = [p for p in clean if p not in valid]
        if invalid:
            raise forms.ValidationError(
                f"Invalid weight values: {', '.join(invalid)}. "
                f"Accepted: {', '.join(v for v, _ in WEIGHT_CHOICES)}"
            )
        if not clean:
            raise forms.ValidationError("Select at least one font weight.")
        return ','.join(clean)

