import re
from django import forms
from .models import Brand
from django.core.exceptions import ValidationError


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "category", "supplier"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name"}),
            "category": forms.TextInput(attrs={"class": "form-control", "id": "category"}),
            "supplier":  forms.Select(attrs={"class": "form-control", "id": "supplier"}),
        }
        labels = {
            "name": "Brand Name",
            "category": "Category",
            "supplier": "Supplier",
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3 or len(name) > 30:
            raise ValidationError("First name must be between 3 and 30 characters")
        return name

    def clean_supplier(self):
        supplier = self.cleaned_data["supplier"]
        if supplier is None:
            raise ValidationError("Please select a supplier")
        return supplier
