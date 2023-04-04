from django.db import models

from home.models import CompanyUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='categories')
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
