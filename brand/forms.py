import re
from django import forms
from .models import Brand
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class BrandForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["supplier"].empty_label = _("label:select_supplier")

    class Meta:
        model = Brand
        fields = ["name", "category", "supplier"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name"}),
            "category": forms.TextInput(attrs={"class": "form-control", "id": "category"}),
            "supplier": forms.Select(attrs={"class": "form-control", "id": "supplier"}),
        }
        labels = {
            "name": _('label:brand_name'),
            "category": _('label:category_name'),
            "supplier": _('label:supplier_name'),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3 or len(name) > 30:
            raise ValidationError(_('message:brand_name_length_error'))
        return name

    def clean_supplier(self):
        supplier = self.cleaned_data["supplier"]
        if supplier is None:
            raise ValidationError(_('message:supplier_name_error'))
        return supplier
