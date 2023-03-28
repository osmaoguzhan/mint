from django.urls import path
from . import views

urlpatterns = [
    path('brands/', views.BrandListView.as_view(), name='brands.list'),
    path('brands/<int:pk>/delete/', views.BrandDeleteView.as_view(), name='brands.delete'),
    path('brands/<int:pk>/update/', views.BrandUpdateView.as_view(), name='brands.update'),
    path('brands/create/', views.BrandCreateView.as_view(), name='brands.create'),
]
