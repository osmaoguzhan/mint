import re
from django import forms
from .models import Supplier
from django.core.exceptions import ValidationError


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "email", "phone", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name"}),
            "email": forms.TextInput(attrs={"class": "form-control", "id": "email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "id": "phone"}),
            "address": forms.Textarea(attrs={"class": "form-control", "id": "address", "rows": 3}),
        }
        labels = {
            "name": "Supplier Name",
            "email": "Email",
            "phone": "Phone",
            "address": "Address",
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3 or len(name) > 30:
            raise ValidationError("Supplier name must be between 3 and 30 characters")
        return name

    def clean_email(self):
        regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        email = self.cleaned_data["email"]
        if not re.fullmatch(regex, email):
            raise ValidationError("Email format is not valid.")
        return email

    def clean_phone(self):
        regex = re.compile(r"(?:\+ *)?\d[\d\- ]{7,}\d")
        phone = self.cleaned_data["phone"]
        if not re.fullmatch(regex, phone):
            raise ValidationError("Phone Number format is not valid.")
        return phone

    def clean_address(self):
        address = self.cleaned_data["address"]
        if len(address) < 15 or len(address) > 100:
            raise ValidationError("Address must be between 15 and 100 characters")
        return address
