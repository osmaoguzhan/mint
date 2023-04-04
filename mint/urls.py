from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('customer.urls')),
    path('', include('brand.urls')),
    path('', include('supplier.urls')),
    path('', include('product.urls')),
]
