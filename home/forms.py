from django.contrib.auth.forms import AuthenticationForm, UsernameField, ReadOnlyPasswordHashField, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
from home.models import CompanyUser
import re


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={
            'id': 'email',
            'class': 'form-control form-control-lg',
            'placeholder': 'Email Address',
            # 'type': 'email', # TODO - after signup form is done, type email
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'id': 'password',
            'class': 'form-control form-control-lg',
            'placeholder': 'Password',
        }
    ))


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    company_name = forms.CharField(
        label='Company Name',
        widget=forms.TextInput(attrs={'placeholder': 'Company Name'})
    )
    phone_number = forms.CharField(
        label='Phone Number',
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    website = forms.CharField(
        label='Website',
        widget=forms.TextInput(attrs={'placeholder': 'Website (Optional)'}),
        required=False
    )
    address = forms.CharField(
        label='Address',
        widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 5})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password Confirmation'})
    )

    class Meta:
        model = CompanyUser
        fields = ('email', 'company_name', 'phone_number', 'website', 'address')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6 or len(password1) > 20:
            raise ValidationError("Password must be between 6 and 20 characters")
        if password1.isdigit():
            raise ValidationError("Password must contain at least one letter")
        if password1.isalpha():
            raise ValidationError("Password must contain at least one number")
        if password1.islower():
            raise ValidationError("Password must contain at least one uppercase letter")
        if password1.isupper():
            raise ValidationError("Password must contain at least one lowercase letter")
        if password1.isalnum():
            raise ValidationError("Password must contain at least one special character")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        if not re.fullmatch(regex, email):
            raise ValidationError("Email format is not valid.")
        if CompanyUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        if CompanyUser.objects.filter(company_name=company_name).exists():
            raise ValidationError("Company name already exists")
        elif len(company_name) < 3 or len(company_name) > 255:
            raise ValidationError("Company name must be between 3 and 255 characters")
        return company_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        regex = re.compile(r"^\+?[1-9][0-9]{7,14}$")
        if not re.fullmatch(regex, phone_number):
            raise ValidationError("Phone Number format is not valid.")
        elif CompanyUser.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Phone number already exists")
        return phone_number

    def clean_website(self):
        website = self.cleaned_data.get("website")
        regex = re.compile(r"^(http|https)://[a-zA-Z0-9]+.[a-zA-Z0-9]+.[a-zA-Z0-9]+")
        if website != "":
            if not re.fullmatch(regex, website):
                raise ValidationError("Website format is not valid.")
            elif CompanyUser.objects.filter(website=website).exists():
                raise ValidationError("Website already exists")
        return website

    def clean_address(self):
        address = self.cleaned_data.get("address")
        if address == "":
            raise ValidationError("Address is required")
        elif len(address) < 3 or len(address) > 255:
            raise ValidationError("Address must be between 3 and 255 characters")
        return address

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    company_name = forms.CharField(
        label='Company Name',
        widget=forms.TextInput(attrs={'placeholder': 'Company Name'})
    )
    phone_number = forms.CharField(
        label='Phone Number',
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    website = forms.CharField(
        label='Website',
        widget=forms.TextInput(attrs={'placeholder': 'Website (Optional)'}),
        required=False
    )
    address = forms.CharField(
        label='Address',
        widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 5})
    )

    class Meta:
        model = CompanyUser
        fields = ('email', 'company_name', 'phone_number', 'website', 'address')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CompanyUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError("Email already exists")
        return email

    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        if CompanyUser.objects.filter(company_name=company_name).exclude(id=self.instance.id).exists():
            raise ValidationError("Company name already exists")
        elif len(company_name) < 3 or len(company_name) > 255:
            raise ValidationError("Company name must be between 3 and 255 characters")
        return company_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if CompanyUser.objects.filter(phone_number=phone_number).exclude(id=self.instance.id).exists():
            raise ValidationError("Phone number already exists")
        return phone_number

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website != "":
            regex = re.compile(r"^(http|https)://[a-zA-Z0-9]+.[a-zA-Z0-9]+.[a-zA-Z0-9]+")
            if not re.fullmatch(regex, website):
                raise ValidationError("Website format is not valid.")
            elif CompanyUser.objects.filter(website=website).exclude(id=self.instance.id).exists():
                raise ValidationError("Website already exists")
        return website

    def clean_address(self):
        address = self.cleaned_data.get("address")
        if address == "":
            raise ValidationError("Address is required")
        elif len(address) < 3 or len(address) > 255:
            raise ValidationError("Address must be between 3 and 255 characters")
        return address
