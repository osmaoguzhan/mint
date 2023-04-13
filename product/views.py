from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from utils import queryParser
from .forms import ProductForm
from .models import Product

LIST_PATH = '/products/'


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'table_template.html'
    context_object_name = 'table_data'
    extra_context = {
        'header_data': [
            {'id': 'id', 'header': 'ID'},
            {'id': 'name', 'header': 'Name'},
            {'id': 'description', 'header': 'Description'},
            {'id': 'amount', 'header': 'Amount'},
            {'id': 'unit', 'header': 'Unit'},
            {'id': 'price', 'header': 'Price'},
            {'id': 'brand', 'header': 'Brand'},
            {'id': 'created', 'header': 'Created'}
        ],
        'title': 'Products',
        'create_path': 'create/',
        'update_path': 'update/',
        'delete_action': 'product',
        'not_found_text': 'No products found!',
        'add_new_text': 'Add a new product'
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


class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    success_url = LIST_PATH
    template_name = 'form_template.html'
    success_message = '%(name)s is successfully updated!'
    form_class = ProductForm
    extra_context = {'submit_btn': 'Update', 'title': 'Update Product', 'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
            brand=self.object.brand
        )


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    success_url = LIST_PATH
    template_name = 'form_template.html'
    form_class = ProductForm
    extra_context = {'submit_btn': 'Create', 'title': 'Create a Product', 'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user
        self.object.save()
        messages.success(self.request,
                         f"{self.object.name} is successfully added with the brand {self.object.brand}!")
        return HttpResponseRedirect(self.get_success_url())


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = LIST_PATH
    login_url = settings.LOGIN_URL
