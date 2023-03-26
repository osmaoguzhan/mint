from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.CustomerListView.as_view(), name='customers.list'),
    path('customers/<int:pk>/delete', views.CustomerDeleteView.as_view(), name='customers.delete'),
    path('customers/<int:pk>/update', views.CustomerUpdateView.as_view(), name='customers.update'),
    path('customers/create', views.CustomerCreateView.as_view(), name='customers.create'),
]
