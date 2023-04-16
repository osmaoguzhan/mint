from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Product


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["brand"].empty_label = _("label:select_brand")

    class Meta:
        model = Product
        fields = ["name", "description", "amount", "unit", "price", "brand"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "id": "description", "rows": 3}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "id": "amount"}),
            "unit": forms.TextInput(attrs={"class": "form-control", "id": "unit"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "id": "price"}),
            "brand": forms.Select(attrs={"class": "form-control", "id": "brand", "required": False}),
        }
        labels = {
            "name": _('label:name'),
            "description": _('label:description'),
            "amount": _('label:amount'),
            "unit": _('label:unit'),
            "price": _('label:price'),
            "brand": _('label:brand_name'),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3 or len(name) > 30:
            raise ValidationError(_('message:product_name_length_error'))
        if self.instance.pk:
            if self.user.products.filter(name=name).exclude(
                    pk=self.instance.pk).exists():
                raise ValidationError(_('message:product_exists_error'))
        else:
            if self.user.products.filter(name=name).exists():
                raise ValidationError(_('message:product_exists_error'))
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        if len(description) < 3 or len(description) > 100:
            raise ValidationError(_('message:product_description_length_error'))
        return description

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0 or amount > 99999999 or amount is None:
            raise ValidationError(_('message:product_amount_error'))
        return amount

    def clean_unit(self):
        unit = self.cleaned_data["unit"]
        if len(unit) < 1 or len(unit) > 10:
            raise ValidationError(_('message:product_unit_length_error'))
        elif not unit.isalpha():
            raise ValidationError(_('message:product_unit_error'))
        return unit

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0 or price > 99999999:
            raise ValidationError(_('message:product_price_error'))
        return price

    def clean_brand(self):
        brand = self.cleaned_data["brand"]
        if brand is None:
            raise ValidationError(_('message:product_brand_error'))
        return brand
