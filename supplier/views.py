from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DeleteView, UpdateView, CreateView

from utils import queryParser
from .forms import SupplierForm
from .models import Supplier

LIST_PATH = '/suppliers/'


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'table_template.html'
    context_object_name = 'table_data'
    extra_context = {
        'header_data': [
            {'id': 'id', 'header': 'ID'},
            {'id': 'name', 'header': 'Supplier Name'},
            {'id': 'email', 'header': 'Email'},
            {'id': 'phone', 'header': 'Phone Number'},
            {'id': 'address', 'header': 'Address'},
            {'id': 'created', 'header': 'Created'}
        ],
        'title': 'Suppliers',
        'create_path': 'create/',
        'update_path': 'update/',
        'delete_action': 'supplier',
        'not_found_text': 'No suppliers found!',
        'add_new_text': 'Add a new supplier'
    }
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        query, order_by, value = queryParser.queryParser(self, 'name')
        print(self.request.user.suppliers)
        if query and query != '':
            return self.request.user.suppliers.filter(name__icontains=query).order_by(
                order_by) or self.request.user.suppliers.filter(
                email__icontains=query).order_by(order_by) or self.request.user.suppliers.filter(
                phone__icontains=query).order_by(order_by) or self.request.user.suppliers.filter(
                address__icontains=query).order_by(order_by) or self.request.user.suppliers.filter(
                created__icontains=query).order_by(order_by)
        return self.request.user.suppliers.all().order_by(order_by)


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    success_url = LIST_PATH
    login_url = settings.LOGIN_URL


class SupplierUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Supplier
    success_url = LIST_PATH
    template_name = 'form_template.html'
    success_message = '%(name)s successfully updated!'
    form_class = SupplierForm
    extra_context = {'submit_btn': 'Update', 'title': 'Update Supplier', 'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    success_url = LIST_PATH
    template_name = 'form_template.html'
    form_class = SupplierForm
    extra_context = {'submit_btn': 'Create', 'title': 'Create Supplier', 'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user
        self.object.save()
        messages.success(self.request,
                         f"{self.object.name} successfully added!")
        return HttpResponseRedirect(self.get_success_url())
