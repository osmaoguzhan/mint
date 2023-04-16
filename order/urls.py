from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='orders.list'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='orders.delete'),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name='orders.update'),
    path('orders/create/', views.OrderCreateView.as_view(), name='orders.create'),
]