from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
