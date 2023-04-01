from django.db import models
from home.models import CompanyUser


class Supplier(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='suppliers', blank=True,
                                null=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
