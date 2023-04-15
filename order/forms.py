from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Order


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].empty_label = _("label:select_product")
        self.fields["product"].required = False
        self.fields["customer"].empty_label = _("label:select_customer")
        self.fields["customer"].required = False

    class Meta:
        model = Order
        fields = ["name", "description", "amount", "price", "product", "customer"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "id": "description", "rows": 3}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "id": "amount"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "id": "price"}),
            "product": forms.Select(attrs={"class": "form-control", "id": "product", "required": False}),
            "customer": forms.Select(attrs={"class": "form-control", "id": "customer", "required": False}),
        }
        labels = {
            "name": _('label:name'),
            "description": _('label:description'),
            "amount": _('label:amount'),
            "price": _('label:price'),
            "product": _('label:product_name'),
            "customer": _('label:customer_name'),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3 or len(name) > 30:
            raise ValidationError(_('message:order_name_error'))
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        if len(description) < 3 or len(description) > 100:
            raise ValidationError(_('message:order_description_error'))
        return description

    #
    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0 or amount > 99999999 or amount is None:
            raise ValidationError(_('message:order_amount_error'))
        return amount

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0 or price > 99999999:
            raise ValidationError(_('message:order_price_error'))
        return price

    #
    def clean_product(self):
        product = self.cleaned_data["product"]
        if product is None:
            raise ValidationError(_('message:order_product_error'))
        return product

    def clean_customer(self):
        customer = self.cleaned_data["customer"]
        if customer is None:
            raise ValidationError(_('message:order_customer_error'))
        return customer
