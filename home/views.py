from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, CreateView, UserChangeView
from django.contrib.auth.views import LoginView, LogoutView
from .admin import UserCreationForm
from django.shortcuts import redirect, render
from .forms import LoginForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginPageView(LoginView):
    template_name = 'home/login.html'
    authentication_form = LoginForm
    extra_context = {'title': 'Login'}

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/brands/')
        return super().get(request, *args, **kwargs)


class LogoutInterfaceView(LogoutView):
    pass


class HomeView(TemplateView):
    template_name = 'home/welcome.html'
    extra_context = {'title': 'Home'}


class SignupView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'home/signup.html'
    extra_context = {'title': 'Signup'}
    success_url = '/login/'
    success_message = 'Account created successfully'


class CustomUserChangeView(LoginRequiredMixin, SuccessMessageMixin, UserChangeView):
    login_url = '/login/'
    form_class = UserChangeForm
    template_name = 'user_change.html'
    success_url = reverse_lazy('profile')
    success_message = "User updated successfully"
