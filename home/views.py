from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .admin import UserCreationForm
from django.shortcuts import redirect, render
from .forms import LoginForm, UserChangeForm, CustomUserChangeForm
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
    success_url = reverse_lazy('login')
    success_message = 'Account created successfully'


class CustomUserChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = '/login/'
    form_class = CustomUserChangeForm
    template_name = 'home/profile.html'
    success_url = reverse_lazy('user_change')
    success_message = "User updated successfully"

    def get_object(self):
        return self.request.user
