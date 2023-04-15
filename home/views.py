from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import activate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView

from category.models import Category
from .admin import UserCreationForm
from django.shortcuts import redirect
from .forms import LoginForm


class LoginPageView(LoginView):
    template_name = 'home/login.html'
    authentication_form = LoginForm
    extra_context = {'title': 'Login'}

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/dashboard/')
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


class DashboardView(TemplateView):
    template_name = 'home/dashboard.html'
    context_object_name = 'analytics'
    extra_context = {'title': 'Dashboard'}

    def get(self, request, *args, **kwargs):
        # get categories with name
        self.extra_context['analytics'] = {
            'customer_count': self.request.user.customers.count(),
            'product_count': self.request.user.products.count(),
            'supplier_count': self.request.user.suppliers.count(),
            'brands': self.request.user.brands.all(),
            'categories': Category.objects.filter(company=self.request.user)
        }
        if not self.request.user.is_authenticated:
            return redirect('/login/')
        return super().get(request, *args, **kwargs)
