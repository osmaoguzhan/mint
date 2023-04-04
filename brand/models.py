from django.db import models
from home.models import CompanyUser
from supplier.models import Supplier


class Brand(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='suppliers', null=True, blank=True)
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='brands', null=True, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
