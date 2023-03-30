from django.db import models
from home.models import CompanyUser


class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    company = models.ForeignKey(CompanyUser, on_delete=models.DO_NOTHING, related_name='brands')
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
