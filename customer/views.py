from django.http import HttpResponseRedirect
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from .models import Customer
from .forms import CustomerForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class CustomerListView(ListView):
    model = Customer
    template_name = 'customer/list.html'
    context_object_name = 'customers'
    extra_context = {
        'title': 'Customers',
    }

    def get_queryset(self):
        query = self.request.GET.get('query')
        order_by = self.request.GET.get('order_by')
        value = self.request.GET.get('value')
        if order_by is None or order_by == '':
            order_by = 'name'
        if value is None or value == '':
            value = 'asc'
        if value == 'desc':
            order_by = '-' + order_by
        if query and query != '':
            return Customer.objects.filter(name__icontains=query).order_by(order_by) or Customer.objects.filter(
                surname__icontains=query).order_by(order_by) or Customer.objects.filter(
                email__icontains=query).order_by(order_by) or Customer.objects.filter(
                phone__icontains=query).order_by(order_by) or Customer.objects.filter(
                address__icontains=query).order_by(order_by)
        return Customer.objects.all().order_by(order_by)


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = '/customers/'


class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    success_url = '/customers/'
    template_name = 'customer/customer_form.html'
    success_message = '%(name)s %(surname)s successfully updated!'
    form_class = CustomerForm
    extra_context = {'submit_btn': 'Update', 'title': 'Update Customer'}

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
            surname=self.object.surname,
        )


class CustomerCreateView(CreateView):
    model = Customer
    success_url = '/customers/'
    template_name = 'customer/customer_form.html'
    form_class = CustomerForm
    extra_context = {'submit_btn': 'Create', 'title': 'Create Customer'}

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request,
                         f"{self.object.name} {self.object.surname} successfully added!")
        return HttpResponseRedirect(self.get_success_url())
