from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='products.list'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='products.delete'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='products.update'),
    path('products/create/', views.ProductCreateView.as_view(), name='products.create'),
]
