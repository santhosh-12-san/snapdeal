from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Auth Views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # OTP Views (Matches views.py correctly now)
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_otp_login, name='verify_otp'),

    # Address Views
    path('address/add/', views.add_address, name='add_address'),
    path('address/', views.address_book, name='address_book'),
    path('check-user/', views.check_user_exists, name='check_user'),
    path('address/add/', views.add_address, name='add_address'),
    path('address/edit/<int:address_id>/', views.edit_address, name='edit_address'),
    path('select-address/', views.select_address, name='select_address'),
    
]