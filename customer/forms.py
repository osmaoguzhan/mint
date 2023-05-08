import re
from django import forms
from .models import Customer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "surname", "email", "phone", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name", "automation-id": "customer-name", "placeholder": _("label:firstname")}),
            "surname": forms.TextInput(attrs={"class": "form-control", "id": "surname", "automation-id": "customer-surname", "placeholder": _("label:surname")}),
            "email": forms.TextInput(attrs={"class": "form-control", "id": "email", "automation-id": "customer-email", "placeholder": _("label:email")}),
            "phone": forms.TextInput(attrs={"class": "form-control", "id": "phone", "automation-id": "customer-phone", "placeholder": _("label:phone_number")}),
            "address": forms.Textarea(attrs={"class": "form-control", "id": "address", "rows": 3, "automation-id": "customer-address", "placeholder": _("label:address")}),
        }
        labels = {
            "name": _("label:firstname"),
            "surname": _("label:surname"),
            "email": _("label:email"),
            "phone": _("label:phone_number"),
            "address": _("label:address"),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3 or len(name) > 30:
            raise ValidationError(_("message:firstname_length"))
        elif name.isalpha() is False:
            raise ValidationError(_("message:firstname_letters_include"))
        return name

    def clean_surname(self):
        surname = self.cleaned_data["surname"]
        if len(surname) < 3 or len(surname) > 30:
            raise ValidationError(_("message:surname_length"))
        elif surname.isalpha() is False:
            raise ValidationError(_("message:surname_letters_include"))
        return surname

    def clean_email(self):
        regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        email = self.cleaned_data["email"]
        if not re.fullmatch(regex, email):
            raise ValidationError(_("message:email_format"))
        return email

    def clean_phone(self):
        regex = re.compile(r"(?:\+ *)?\d[\d\- ]{7,}\d")
        phone = self.cleaned_data["phone"]
        if not re.fullmatch(regex, phone):
            raise ValidationError(_("message:phone_format"))
        return phone

    def clean_address(self):
        address = self.cleaned_data["address"]
        if len(address) < 15 or len(address) > 100:
            raise ValidationError(_("message:address_length"))
        return address
