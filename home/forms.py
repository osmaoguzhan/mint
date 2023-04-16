from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.core.exceptions import ValidationError
from home.models import CompanyUser
import re
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={
            'id': 'email',
            'class': 'form-control form-control-lg',
            'placeholder': _('label:email_address'),
            'type': 'email'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'id': 'password',
            'class': 'form-control form-control-lg',
            'placeholder': _('label:password'),
        }
    ))


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('label:email_address'),
        widget=forms.EmailInput(attrs={'placeholder': _('label:email_address')})
    )
    company_name = forms.CharField(
        label=_('label:company_name'),
        widget=forms.TextInput(attrs={'placeholder': _('label:company_name')})
    )
    phone_number = forms.CharField(
        label=_('label:phone_number'),
        widget=forms.TextInput(attrs={'placeholder': _('label:phone_number')})
    )
    website = forms.CharField(
        label=_('label:website_optional'),
        widget=forms.TextInput(attrs={'placeholder': _('label:website_optional')}),
        required=False
    )
    address = forms.CharField(
        label=_('label:address'),
        widget=forms.Textarea(attrs={'placeholder': _('label:address'), 'rows': 5})
    )
    password1 = forms.CharField(
        label=_('label:password'),
        widget=forms.PasswordInput(attrs={'placeholder': _('label:password')})
    )
    password2 = forms.CharField(
        label=_('label:password_confirmation'),
        widget=forms.PasswordInput(
            attrs={'placeholder': _('label:password_confirmation')})
    )

    class Meta:
        model = CompanyUser
        fields = ('email', 'company_name', 'phone_number', 'website', 'address')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6 or len(password1) > 20:
            raise ValidationError(_("message:password_length_error"))
            # raise ValidationError("Password must be between 6 and 20 characters")
        if password1.isdigit():
            raise ValidationError(_("message:password_at_least_one_letter"))
            # raise ValidationError("Password must contain at least one letter")
        if password1.isalpha():
            raise ValidationError(_("message:password_at_least_one_number"))
            # raise ValidationError("Password must contain at least one number")
        if password1.islower():
            raise ValidationError(_("message:password_at_least_one_uppercase"))
            # raise ValidationError("Password must contain at least one uppercase letter")
        if password1.isupper():
            raise ValidationError(_("message:password_at_least_one_lowercase"))
            # raise ValidationError("Password must contain at least one lowercase letter")
        if password1.isalnum():
            raise ValidationError(_("message:password_at_least_one_special_character"))
            # raise ValidationError("Password must contain at least one special character")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("message:passwords_do_not_match"))
            # raise ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        if not re.fullmatch(regex, email):
            raise ValidationError(_("message:email_format"))
        if CompanyUser.objects.filter(email=email).exists():
            raise ValidationError(_("message:email_already_exists"))
        return email

    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        if CompanyUser.objects.filter(company_name=company_name).exists():
            raise ValidationError(_("message:company_name_already_exists"))
        elif len(company_name) < 3 or len(company_name) > 255:
            raise ValidationError(_("message:company_name_length_error"))
        return company_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        regex = re.compile(r"^\+?[1-9][0-9]{7,14}$")
        if not re.fullmatch(regex, phone_number):
            raise ValidationError(_("message:phone_format"))
        elif CompanyUser.objects.filter(phone_number=phone_number).exists():
            raise ValidationError(_("message:phone_number_already_exists"))
        return phone_number

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website != "":
            regex = re.compile(r"^(http|https)://[a-zA-Z0-9]+.[a-zA-Z0-9]+.[a-zA-Z0-9]+")
            if not re.fullmatch(regex, website):
                raise ValidationError(_('message:website_format_is_not_valid'))
            elif CompanyUser.objects.filter(website=website).exists():
                raise ValidationError(_('message:website_already_exists'))
        return website

    def clean_address(self):
        address = self.cleaned_data.get("address")
        if address == "":
            raise ValidationError(_('message:address_is_required'))
        elif len(address) < 3 or len(address) > 255:
            raise ValidationError(_('message:company_address_length_error'))
        return address

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('label:email'),
        widget=forms.EmailInput(
            attrs={'placeholder': _('label:email'), 'class': 'form-control', 'id': 'email', 'readonly': 'readonly',
                   'title': _('message:please_contact_admin_to_change_email.')})
    )
    company_name = forms.CharField(
        label=_('label:company_name'),
        widget=forms.TextInput(
            attrs={'placeholder': _('label:company_name'), 'class': 'form-control', 'id': 'company_name',
                   'readonly': 'readonly', 'title': _('message:please_contact_admin_to_change_company_name')})
    )
    phone_number = forms.CharField(
        label=_('label:phone_number'),
        widget=forms.TextInput(
            attrs={'placeholder': _('label:phone_number'), 'class': 'form-control', 'id': 'phone_number'})
    )
    website = forms.CharField(
        label=_('label:website_optional'),
        widget=forms.TextInput(
            attrs={'placeholder': _('label:website_optional'), 'class': 'form-control', 'id': 'website'}),
        required=False
    )
    address = forms.CharField(
        label=_('label:address'),
        widget=forms.Textarea(
            attrs={'placeholder': _('label:address'), 'rows': 5, 'class': 'form-control', 'id': 'address'})
    )

    class Meta:
        model = CompanyUser
        fields = ('email', 'company_name', 'phone_number', 'website', 'address')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if self.instance.email != email:
            raise ValidationError(_('message:email_cannot_be_changed'))
        return email

    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        if self.instance.company_name != company_name:
            raise ValidationError(_('message:company_name_cannot_be_changed'))
        return company_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        regex = re.compile(r"^\+?[1-9][0-9]{7,14}$")
        if not re.fullmatch(regex, phone_number):
            raise ValidationError(_("message:phone_number_format"))
        elif CompanyUser.objects.filter(phone_number=phone_number).exclude(id=self.instance.id).exists():
            raise ValidationError(_("message:phone_number_already_exists"))
        return phone_number

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website != "":
            regex = re.compile(r"^(http|https)://[a-zA-Z0-9]+.[a-zA-Z0-9]+.[a-zA-Z0-9]+")
            if not re.fullmatch(regex, website):
                raise ValidationError(_('message:website_format_is_not_valid'))
            elif CompanyUser.objects.filter(website=website).exclude(id=self.instance.id).exists():
                raise ValidationError(_('message:website_already_exists'))
        return website

    def clean_address(self):
        address = self.cleaned_data.get("address")
        if address == "":
            raise ValidationError(_('message:address_is_required'))
        elif len(address) < 3 or len(address) > 255:
            raise ValidationError(_('message:company_address_length_error'))
        return address
