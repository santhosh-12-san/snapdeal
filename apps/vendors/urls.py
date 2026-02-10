from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('dashboard/', views.vendor_dashboard, name='dashboard'),
    path('add-product/', views.add_product, name='add_product'),
]