from django.urls import path
from . import views

app_name = 'core'  # <--- This is why we need 'core:' in the template

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'), # Ensure this line is here
]