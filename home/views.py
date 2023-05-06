from datetime import timedelta

from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView

from category.models import Category
from order.models import Order
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
            return redirect('/dashboard/')
        return super().get(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('django_language', self.request.LANGUAGE_CODE)
        return response


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


class DashboardView(TemplateView):
    template_name = 'home/dashboard.html'
    context_object_name = 'analytics'
    extra_context = {'title': _('label:dashboard')}

    def get(self, request, *args, **kwargs):
        income = self.request.user.orders.filter(
            created__gte=timezone.now() - timedelta(days=7)
        ).values('created').annotate(
            total_price=Sum('price'),
            total_amount=Sum('amount')
        ).order_by('created')
        for item in income:
            item['created'] = item['created'].strftime('%d/%m/%Y')
            item['total_price'] = float(item['total_price'])
        product_ids = self.request.user.orders.values('product__id')
        brand_ids = self.request.user.products.filter(id__in=product_ids).values('brand__id')
        categories = self.request.user.brands.filter(id__in=brand_ids).values('category__name').distinct()

        self.extra_context['analytics'] = {
            'customer_count': self.request.user.customers.count(),
            'product_count': self.request.user.products.count(),
            'supplier_count': self.request.user.suppliers.count(),
            'brands': self.request.user.brands.all(),
            'categories': categories,
            'income': income

        }
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        return super().get(request, *args, **kwargs)
