from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .admin import UserCreationForm
from django.shortcuts import redirect
from .forms import LoginForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _


class LoginPageView(LoginView):
    template_name = 'home/login.html'
    authentication_form = LoginForm
    extra_context = {'title': _('label:login')}

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        return super().get(request, *args, **kwargs)


class LogoutInterfaceView(LogoutView):
    pass


class HomeView(TemplateView):
    template_name = 'home/welcome.html'
    extra_context = {'title': _('label:home')}


class SignupView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'home/signup.html'
    extra_context = {'title': _('label:signup')}
    success_url = reverse_lazy('login')
    success_message = _('message:company_created_successfully')


class CustomUserChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = settings.LOGIN_URL
    form_class = CustomUserChangeForm
    template_name = 'form_template.html'
    success_url = reverse_lazy('company_settings')
    success_message = _('message:company_updated_successfully')
    extra_context = {'title': _('label:company_settings'), 'submit_btn': _('label:update_button_text')}

    def get_object(self):
        return self.request.user
