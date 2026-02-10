from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('api/check-pincode/', views.check_pincode, name='check_pincode'), # AJAX API
]