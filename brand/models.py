from django.db import models
from category.models import Category
from home.models import CompanyUser
from supplier.models import Supplier


class Brand(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='suppliers')
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='brands')
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
