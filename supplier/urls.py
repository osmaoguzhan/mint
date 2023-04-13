from django.urls import path
from . import views

urlpatterns = [
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers.list'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='suppliers.delete'),
    path('suppliers/<int:pk>/update/', views.SupplierUpdateView.as_view(), name='suppliers.update'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='suppliers.create'),
]
