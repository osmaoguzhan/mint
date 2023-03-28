import re
from django import forms
from .models import Brand
from django.core.exceptions import ValidationError


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name"}),
            "category": forms.TextInput(attrs={"class": "form-control", "id": "surname"}),
        }
        labels = {
            "name": "Brand Name",
            "category": "Category"
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3 or len(name) > 30:
            raise ValidationError("First name must be between 3 and 30 characters")
        return name
