from django import forms
from .models import Customer
from django.core.exceptions import ValidationError


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'surname', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'id': 'surname'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'id': 'address', 'rows': 3}),
        }
        labels = {
            'name': 'First Name',
            'surname': 'Last Name',
            'email': 'Email',
            'phone': 'Phone',
            'address': 'Address',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3 or len(name) > 30:
            raise ValidationError("First name must be between 3 and 30 characters")
        elif name.isalpha() is False:
            raise ValidationError("First name must include only letters")
        return name

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if len(surname) < 3 or len(surname) > 30:
            raise ValidationError("First name must be between 3 and 30 characters")
        elif surname.isalpha() is False:
            raise ValidationError("First name must include only letters")
        return surname
