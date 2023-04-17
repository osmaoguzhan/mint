from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.formats import date_format
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from utils import queryParser
from .forms import ProductForm
from .models import Product
from django.utils.translation import gettext_lazy as _

LIST_PATH = reverse_lazy('products.list')


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'table_template.html'
    context_object_name = 'table_data'
    extra_context = {
        'header_data': [
            {'id': 'id', 'header': 'ID'},
            {'id': 'name', 'header': _('label:name')},
            {'id': 'description', 'header': _('label:description')},
            {'id': 'amount', 'header': _('label:amount')},
            {'id': 'unit', 'header': _('label:unit')},
            {'id': 'price', 'header': _('label:price')},
            {'id': 'brand', 'header': _('label:brand_name')},
            {'id': 'created', 'header': _('label:created_date')},
        ],
        'title': _('label:products'),
        'create_path': 'create/',
        'update_path': 'update/',
        'delete_action': 'product',
        'not_found_text': _('message:no_products_found'),
        'add_new_text': _('label:add_new_product'),
    }
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        query, order_by, value = queryParser.queryParser(self, 'name')
        if query and query != '':
            return self.request.user.products.filter(name__icontains=query).order_by(
                order_by) or self.request.user.products.filter(
                description__icontains=query).order_by(order_by) or self.request.user.products.filter(
                amount__icontains=query).order_by(order_by) or self.request.user.products.filter(
                unit__icontains=query).order_by(order_by) or self.request.user.products.filter(
                price__icontains=query).order_by(order_by) or self.request.user.products.filter(
                brand__icontains=query).order_by(order_by) or self.request.user.products.filter(
                created__icontains=query).order_by(order_by)
        return self.request.user.products.all().order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        new_context = dict()
        for item in context['table_data']:
            new_context[item.id] = {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'amount': item.amount,
                'unit': item.unit,
                'price': item.price,
                'brand': item.brand,
                'created': date_format(item.created, 'd/m/Y', use_l10n=True)
            }
        context['table_data'] = new_context
        return context


class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    success_url = LIST_PATH
    template_name = 'form_template.html'
    success_message = _("message:product_updated")
    form_class = ProductForm
    extra_context = {'submit_btn': _('label:update_button_text'), 'title': _('label:update_a_product'),
                     'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def get_form_kwargs(self):
        kwargs = super(ProductUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    success_url = LIST_PATH
    template_name = 'form_template.html'
    form_class = ProductForm
    extra_context = {'submit_btn': _('label:create_button_text'), 'title': _('label:create_a_product'),
                     'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user
        self.object.save()
        messages.success(self.request, _("message:product_created"))
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = LIST_PATH
    login_url = settings.LOGIN_URL
