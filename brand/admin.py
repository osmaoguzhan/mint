from django.contrib import admin
from . import models


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created')


admin.site.register(models.Brand, BrandAdmin)
