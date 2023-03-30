from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={
            'id': 'email',
            'class': 'form-control form-control-lg',
            'placeholder': 'Please enter your email',
            # 'type': 'email', # TODO - after signup form is done, type email
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'id': 'password',
            'class': 'form-control form-control-lg',
            'placeholder': 'Please enter your password',
        }
    ))
