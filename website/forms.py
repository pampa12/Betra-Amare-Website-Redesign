from django import forms

from .models import Inquiry


class InquiryForm(forms.ModelForm):
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
