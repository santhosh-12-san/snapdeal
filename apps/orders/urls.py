from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # 1. Cart Actions
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # 2. The Checkout (Triggers the Popup)
    path('checkout/', views.checkout, name='checkout'),
    
    # 3. Success Page (Where popup sends you after payment)
    path('payment/success/', views.payment_success, name='payment_success'),
    
    # 4. Order History
    path('my-orders/', views.my_orders, name='my_orders'),
    path('payment/', views.payment, name='payment'),
    # 3. Order History
    # ... Success & Tracking ...
 
    path('track/<str:order_id>/', views.track_order, name='track_order'), # <
    path('my-orders/', views.my_orders, name='my_orders'),
]