from django.urls import path
from . import views
app_name='users'
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),  # 👈 Default path goes to custom login
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]