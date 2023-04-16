from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Brand
from .forms import BrandForm
from django.contrib import messages
from utils import queryParser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.formats import date_format

LIST_PATH = reverse_lazy('brands.list')


class BrandListView(LoginRequiredMixin, ListView):
    model = Brand
    template_name = 'table_template.html'
    context_object_name = 'table_data'
    extra_context = {
        'header_data': [
            {'id': 'id', 'header': 'ID'},
            {'id': 'name', 'header': _('label:brand_name')},
            {'id': 'category', 'header': _('label:category_name')},
            {'id': 'supplier', 'header': _('label:supplier_name')},
            {'id': 'created', 'header': _('label:created_date')},
        ],
        'title': _('label:brands'),
        'create_path': 'create/',
        'update_path': 'update/',
        'delete_action': 'brand',
        'not_found_text': _('message:no_brands_found'),
        'add_new_text': _('label:add_new_brand'),
    }
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        query, order_by, value = queryParser.queryParser(self, 'name')
        if query and query != '':
            return self.request.user.brands.filter(name__icontains=query).order_by(
                order_by) or self.request.user.brands.filter(
                category__icontains=query).order_by(order_by) or self.request.user.brands.filter(
                supplier__icontains=query).order_by(order_by) or self.request.user.brands.filter(
                created__icontains=query).order_by(order_by)
        return self.request.user.brands.all().order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super(BrandListView, self).get_context_data(**kwargs)
        new_context = dict()

        for item in context['table_data']:
            new_context[item.id] = {
                'id': item.id,
                'name': item.name,
                'category': item.category,
                'supplier': item.supplier,
                'created': date_format(item.created, 'd/m/Y', use_l10n=True)
            }
        context['table_data'] = new_context
        return context


class BrandUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Brand
    success_url = LIST_PATH
    template_name = 'form_template.html'
    success_message = _("message:brand_updated")
    form_class = BrandForm
    extra_context = {'submit_btn': _('label:update_button_text'), 'title': _('label:update_a_brand'),
                     'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL


class BrandCreateView(LoginRequiredMixin, CreateView):
    model = Brand
    success_url = LIST_PATH
    form_class = BrandForm
    template_name = 'form_template.html'
    extra_context = {'submit_btn': _('label:create_button_text'), 'title': _('label:create_a_brand'),
                     'list_path': LIST_PATH}
    login_url = settings.LOGIN_URL

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user
        self.object.save()
        messages.success(self.request, _("message:brand_created"))
        return HttpResponseRedirect(self.get_success_url())

    def get_form(self, form_class=None):
        form = super(BrandCreateView, self).get_form(form_class)
        form.fields['supplier'].queryset = self.request.user.suppliers.all()
        return form


class BrandDeleteView(LoginRequiredMixin, DeleteView):
    model = Brand
    success_url = LIST_PATH
    login_url = settings.LOGIN_URL
