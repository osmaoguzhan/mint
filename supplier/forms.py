import re
from django import forms
from .models import Supplier
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
            "name": _('label:name'),
            "email": _('label:email'),
            "phone": _('label:phone_number'),
            "address": _('label:address'),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3 or len(name) > 30:
            raise ValidationError(_('message:supplier_name_length'))
        return name

    def clean_email(self):
        regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        email = self.cleaned_data["email"]
        if not re.fullmatch(regex, email):
            raise ValidationError(_('message:email_format'))
        return email

    def clean_phone(self):
        regex = re.compile(r"(?:\+ *)?\d[\d\- ]{7,}\d")
        phone = self.cleaned_data["phone"]
        if not re.fullmatch(regex, phone):
            raise ValidationError(_('message:phone_format'))
        return phone

    def clean_address(self):
        address = self.cleaned_data["address"]
        if len(address) < 15 or len(address) > 100:
            raise ValidationError(_('message:address_length'))
        return address
