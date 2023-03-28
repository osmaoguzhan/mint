from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Brand
from .forms import BrandForm
from django.contrib import messages
from utils import queryParser

LIST_PATH = '/brands/'


class BrandListView(ListView):
    model = Brand
    template_name = 'table_template.html'
    context_object_name = 'table_data'
    extra_context = {
        'header_data': [
            {'id': 'id', 'header': 'ID'},
            {'id': 'name', 'header': 'Brand Name'},
            {'id': 'category', 'header': 'Category'},
            {'id': 'created', 'header': 'Created'}
        ],
        'title': 'Brands',
        'create_path': 'create/',
        'update_path': 'update/',
        'delete_action': 'brand',
        'not_found_text': 'No brands found!',
        'add_new_text': 'Add a new brand'
    }

    def get_queryset(self):
        query, order_by, value = queryParser.queryParser(self, 'name')
        if query and query != '':
            return Brand.objects.filter(name__icontains=query).order_by(order_by) or Brand.objects.filter(
                category__icontains=query).order_by(order_by) or Brand.objects.filter(
                created__icontains=query).order_by(order_by)
        return Brand.objects.all().order_by(order_by)


class BrandUpdateView(SuccessMessageMixin, UpdateView):
    model = Brand
    success_url = '/brands'
    template_name = 'form_template.html'
    success_message = '%(name)s is successfully updated!'
    form_class = BrandForm
    extra_context = {'submit_btn': 'Update', 'title': 'Update Brand', 'list_path': LIST_PATH}

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
            category=self.object.category,
        )


class BrandCreateView(CreateView):
    model = Brand
    success_url = '/brands/'
    template_name = 'form_template.html'
    form_class = BrandForm
    extra_context = {'submit_btn': 'Create', 'title': 'Create a Brand', 'list_path': LIST_PATH}

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request,
                         f"{self.object.name} is successfully added with the category {self.object.category}!")
        return HttpResponseRedirect(self.get_success_url())


class BrandDeleteView(DeleteView):
    model = Brand
    success_url = '/brands/'
