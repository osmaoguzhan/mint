from django.contrib import admin

from . import models


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'amount', 'price', 'product', 'customer', 'created')


admin.site.register(models.Order, OrderAdmin)
