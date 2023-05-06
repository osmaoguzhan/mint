from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.formats import date_format
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from utils import queryParser
from .forms import SupplierForm
from .models import Supplier
from django.utils.translation import gettext_lazy as _

LIST_PATH = reverse_lazy('suppliers.list')


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'table_template.html'
    context_object_name = 'table_data'
    paginate_by = 5
    extra_context = {
        'header_data': [
            {'id': 'id', 'header': 'ID'},
            {'id': 'name', 'header': _('label:name')},
            {'id': 'email', 'header': _('label:email')},
            {'id': 'phone', 'header': _('label:phone_number')},
            {'id': 'address', 'header': _('label:address')},
            {'id': 'created', 'header': _('label:created_date')}
        ],
        'title': _('label:suppliers'),
        'create_path': 'create/',
        'update_path': 'update/',
        'delete_action': 'supplier',
        'not_found_text': _('message:supplier_not_found'),
        'add_new_text': _('label:add_new_supplier')
    }
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        query, order_by, value = queryParser.queryParser(self, 'name')
        if query and query != '':
            return self.request.user.suppliers.filter(name__icontains=query).order_by(
                order_by) or self.request.user.suppliers.filter(
                email__icontains=query).order_by(order_by) or self.request.user.suppliers.filter(
                phone__icontains=query).order_by(order_by) or self.request.user.suppliers.filter(
                address__icontains=query).order_by(order_by) or self.request.user.suppliers.filter(
                created__icontains=query).order_by(order_by)
        return self.request.user.suppliers.all().order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super(SupplierListView, self).get_context_data(**kwargs)
        new_context = dict()
        for item in context['table_data']:
            new_context[item.id] = {
                'id': item.id,
                'name': item.name,
                'email': item.email,
                'phone': item.phone,
                'address': item.address,
                'created': date_format(item.created, 'd/m/Y', use_l10n=True)
            }
        context['table_data'] = new_context
        return context


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    success_url = LIST_PATH
    login_url = settings.LOGIN_URL


class SupplierUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Supplier
    success_url = LIST_PATH
    template_name = 'form_template.html'
    success_message = _('message:supplier_updated')
    form_class = SupplierForm
    extra_context = {'submit_btn': _('label:update_button_text'), 'title': _('label:update_a_supplier'),
                     'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL


class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    success_url = LIST_PATH
    template_name = 'form_template.html'
    form_class = SupplierForm
    extra_context = {'submit_btn': _('label:create_button_text'), 'title': _('label:create_a_supplier'),
                     'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user
        self.object.save()
        messages.success(self.request, _('message:supplier_created'))
        return HttpResponseRedirect(self.get_success_url())
