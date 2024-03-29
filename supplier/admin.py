from django.contrib import admin
from . import models


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'company', 'created')


admin.site.register(models.Supplier, SupplierAdmin)
