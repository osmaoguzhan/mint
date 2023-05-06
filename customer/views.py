from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.formats import date_format
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import queryParser
from .models import Customer
from .forms import CustomerForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext_lazy as _

LIST_PATH = reverse_lazy('customers.list')


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'table_template.html'
    context_object_name = 'table_data'
    paginate_by = 5
    extra_context = {
        'header_data': [
            {'id': 'id', 'header': 'ID'},
            {'id': 'name', 'header': _('label:firstname')},
            {'id': 'surname', 'header': _('label:surname')},
            {'id': 'email', 'header': _('label:email')},
            {'id': 'phone', 'header': _('label:phone_number')},
            {'id': 'address', 'header': _('label:address')},
            {'id': 'created', 'header': _('label:created_date')},
        ],
        'title': _('label:customers'),
        'create_path': 'create/',
        'update_path': 'update/',
        'delete_action': 'customer',
        'not_found_text': _('message:customer_not_found'),
        'add_new_text': _('label:add_new_customer'),
    }
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        query, order_by, value = queryParser.queryParser(self, 'name')
        if query and query != '':
            return self.request.user.customers.filter(name__icontains=query).order_by(
                order_by) or self.request.user.customers.filter(
                surname__icontains=query).order_by(order_by) or self.request.user.customers.filter(
                email__icontains=query).order_by(order_by) or self.request.user.customers.filter(
                phone__icontains=query).order_by(order_by) or self.request.user.customers.filter(
                address__icontains=query).order_by(order_by) or self.request.user.customers.filter(
                created__icontains=query).order_by(order_by)
        return self.request.user.customers.all().order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        new_context = dict()
        for item in context['table_data']:
            new_context[item.id] = {
                'id': item.id,
                'name': item.name,
                'surname': item.surname,
                'email': item.email,
                'phone': item.phone,
                'address': item.address,
                'created': date_format(item.created, 'd/m/Y', use_l10n=True)
            }
        context['table_data'] = new_context
        return context


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = '/customers/'
    login_url = settings.LOGIN_URL


class CustomerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Customer
    success_url = '/customers/'
    template_name = 'form_template.html'
    success_message = _("message:customer_updated")
    form_class = CustomerForm
    extra_context = {'submit_btn': _('label:update_button_text'), 'title': _('label:update_a_customer'),
                     'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    success_url = '/customers/'
    template_name = 'form_template.html'
    form_class = CustomerForm
    extra_context = {'submit_btn': _('label:create_button_text'), 'title': _('label:create_a_customer'),
                     'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user
        self.object.save()
        messages.success(self.request, _("message:customer_created"))
        return HttpResponseRedirect(self.get_success_url())
