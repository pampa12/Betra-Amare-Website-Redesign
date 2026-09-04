from django import forms

from .models import Inquiry


class InquiryForm(forms.ModelForm):
    # Honeypot: real visitors never see or fill this field, but many bots do.
    website = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
                "aria-hidden": "true",
                "class": "hp-input",
            }
        ),
    )

    class Meta:
        model = Inquiry
        fields = ["name", "email", "company", "project_type", "budget", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@brand.com", "autocomplete": "email"}),
            "company": forms.TextInput(attrs={"placeholder": "Brand or company (optional)"}),
            "project_type": forms.Select(
                choices=[
                    ("Brand collaboration", "Brand collaboration"),
                    ("UGC / content creation", "UGC / content creation"),
                    ("Modeling", "Modeling"),
                    ("Event / appearance", "Event / appearance"),
                    ("Campaign / photoshoot", "Campaign / photoshoot"),
                    ("Other", "Other"),
                ]
            ),
            "budget": forms.TextInput(attrs={"placeholder": "Budget range (optional)"}),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Brand, deliverables, timeline, usage, and anything else I should know..."
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            raise forms.ValidationError("Unable to submit the form. Please try again.")
        return cleaned_data
