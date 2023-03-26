from django.contrib import admin
from . import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'phone', 'address', 'created')


admin.site.register(models.Customer, CustomerAdmin)
