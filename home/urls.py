from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutInterfaceView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('settings/', views.CustomUserChangeView.as_view(), name='company_settings'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
