from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path('', include('customer.urls')),
    path('', include('brand.urls')),
    path('', include('supplier.urls')),
    path('', include('product.urls')),
    path('', include('order.urls')),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
)
