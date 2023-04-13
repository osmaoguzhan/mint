from django import forms
from django.core.exceptions import ValidationError

from .models import Brand


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "category", "supplier"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name"}),
            "category": forms.Select(attrs={"class": "form-control", "id": "category"}),
            "supplier": forms.Select(attrs={"class": "form-control", "id": "supplier"}),
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

    def clean_category(self):
        category = self.cleaned_data["category"]
        if category is None:
            raise ValidationError("Category must be selected")
        return category

    def clean_supplier(self):
        supplier = self.cleaned_data["supplier"]
        if supplier is None:
            raise ValidationError("Please select a supplier")
        return supplier
