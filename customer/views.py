from django.http import HttpResponseRedirect
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import queryParser
from .models import Customer
from .forms import CustomerForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.conf import settings

LIST_PATH = '/customers/'


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'table_template.html'
    context_object_name = 'table_data'
    extra_context = {
        'header_data': [
            {'id': 'id', 'header': 'ID'},
            {'id': 'name', 'header': 'Firstname'},
            {'id': 'surname', 'header': 'Lastname'},
            {'id': 'email', 'header': 'Email'},
            {'id': 'phone', 'header': 'Phone Number'},
            {'id': 'address', 'header': 'Address'},
            {'id': 'created', 'header': 'Created'}
        ],
        'title': 'Customers',
        'create_path': 'create/',
        'update_path': 'update/',
        'delete_action': 'customer',
        'not_found_text': 'No customers found!',
        'add_new_text': 'Add a new customer'
    }
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        query, order_by, value = queryParser.queryParser(self, 'name')
        print(self.request.user.customers)
        if query and query != '':
            return self.request.user.customers.filter(name__icontains=query).order_by(
                order_by) or self.request.user.customers.filter(
                surname__icontains=query).order_by(order_by) or self.request.user.customers.filter(
                email__icontains=query).order_by(order_by) or self.request.user.customers.filter(
                phone__icontains=query).order_by(order_by) or self.request.user.customers.filter(
                address__icontains=query).order_by(order_by) or self.request.user.customers.filter(
                created__icontains=query).order_by(order_by)
        return self.request.user.customers.all().order_by(order_by)


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = '/customers/'
    login_url = settings.LOGIN_URL


class CustomerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Customer
    success_url = '/customers/'
    template_name = 'form_template.html'
    success_message = '%(name)s %(surname)s successfully updated!'
    form_class = CustomerForm
    extra_context = {'submit_btn': 'Update', 'title': 'Update Customer', 'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
            surname=self.object.surname,
        )


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    success_url = '/customers/'
    template_name = 'form_template.html'
    form_class = CustomerForm
    extra_context = {'submit_btn': 'Create', 'title': 'Create Customer', 'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user
        self.object.save()
        messages.success(self.request,
                         f"{self.object.name} {self.object.surname} successfully added!")
        return HttpResponseRedirect(self.get_success_url())
