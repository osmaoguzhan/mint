from django.db import models

from home.models import CompanyUser
from product.models import Product
from customer.models import Customer


class Order(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customers')
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
