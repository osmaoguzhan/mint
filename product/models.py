from django.db import models

from brand.models import Brand
from home.models import CompanyUser


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brands')
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='products')
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
