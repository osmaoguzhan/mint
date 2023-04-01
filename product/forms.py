from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "unit", "price", "brand"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "id": "description"}),
            "unit": forms.TextInput(attrs={"class": "form-control", "id": "unit"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "id": "price"}),
            "brand": forms.Select(attrs={"class": "form-control", "id": "brand"}),
        }
        labels = {
            "name": "Name",
            "description": "Description",
            "unit": "Unit",
            "price": "Price",
            "brand": "Brand"
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3 or len(name) > 30:
            raise ValidationError("Product name must be between 3 and 30 characters")
        elif Product.objects.filter(name=name).exists():
            raise ValidationError("Product with this name already exists")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        if len(description) < 3 or len(description) > 100:
            raise ValidationError("Description must be between 3 and 100 characters")
        return description

    def clean_unit(self):
        unit = self.cleaned_data["unit"]
        if len(unit) < 1 or len(unit) > 10:
            raise ValidationError("Unit must be between 1 and 10 characters")
        return unit

    def clean_price(self):
        price = self.cleaned_data["price"]
        if 0 > price > 99999999:
            raise ValidationError("Price must be greater than 0 and less than 99999999")
        return price

    def clean_brand(self):
        brand = self.cleaned_data["brand"]
        if brand is None:
            raise ValidationError("Brand must be selected")
        return brand
