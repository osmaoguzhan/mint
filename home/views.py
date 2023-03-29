from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from .forms import LoginForm


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
