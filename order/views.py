from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.utils.formats import date_format
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from utils import queryParser
from .forms import OrderForm
from .models import Order
from django.utils.translation import gettext_lazy as _

LIST_PATH = '/orders/'


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'table_template.html'
    context_object_name = 'table_data'
    extra_context = {
        'header_data': [
            {'id': 'id', 'header': 'ID'},
            {'id': 'name', 'header': _('label:name')},
            {'id': 'description', 'header': _('label:description')},
            {'id': 'amount', 'header': _('label:amount')},
            {'id': 'price', 'header': _('label:price')},
            {'id': 'product', 'header': _('label:product_name')},
            {'id': 'customer', 'header': _('label:customer_name')},
            {'id': 'created', 'header': _('label:created_date')},
        ],
        'title': _('label:orders'),
        'create_path': 'create/',
        'update_path': 'update/',
        'delete_action': 'order',
        'not_found_text': _('message:order_not_found'),
        'add_new_text': _('label:add_new_order'),
    }
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        query, order_by, value = queryParser.queryParser(self, 'name')
        products = self.request.user.products.all()
        if query and query != '':
            return Order.objects.filter(product__in=products, name__icontains=query).order_by(
                order_by) or Order.objects.filter(
                product__in=products, description__icontains=query).order_by(order_by) or Order.objects.filter(
                product__in=products, amount__icontains=query).order_by(order_by) or Order.objects.filter(
                product__in=products, price__icontains=query).order_by(order_by) or Order.objects.filter(
                product__in=products, created__icontains=query).order_by(order_by)
        else:
            return Order.objects.filter(product__in=products).order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        new_context = dict()
        for item in context['table_data']:
            new_context[item.id] = {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'amount': item.amount,
                'price': item.price,
                'product': item.product,
                'customer': item.customer,
                'created': date_format(item.created, 'd/m/Y', use_l10n=True)
            }
        context['table_data'] = new_context
        return context


class OrderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Order
    success_url = LIST_PATH
    template_name = 'form_template.html'
    success_message = _('message:order_updated_successfully')
    form_class = OrderForm
    extra_context = {'submit_btn': _('label:update_button_text'), 'title': _('label:update_order'),
                     'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    success_url = LIST_PATH
    template_name = 'form_template.html'
    form_class = OrderForm
    extra_context = {'submit_btn': _('label:create_button_text'), 'title': _('label:create_order'),
                     'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request, _('message:order_created_successfully'))
        return HttpResponseRedirect(self.get_success_url())


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = LIST_PATH
    login_url = settings.LOGIN_URL
