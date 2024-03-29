from django.contrib import admin

from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'amount', 'unit', 'price', 'brand', 'created')


admin.site.register(models.Product, ProductAdmin)
