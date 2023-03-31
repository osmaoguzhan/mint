from django.db import models
from home.models import CompanyUser


class Customer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='customers', blank=True,
                                null=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name + ' ' + self.surname
