from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from apps.orders.models import Order
from .models import Payment

def initiate_payment(request, order_id):
    """Step 1: Prepare payment data"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # In a real app, create order on Razorpay API here
    amount_in_paisa = int(order.total_amount * 100)
    
    context = {
        'order': order,
        'razorpay_order_id': 'order_fake_123456', # Dummy ID for testing
        'razorpay_key': 'rzp_test_YOUR_KEY',
        'amount': amount_in_paisa
    }
    return render(request, 'payments/process.html', context)

@csrf_exempt
def payment_callback(request):
    """Step 2: Handle response from Payment Gateway"""
    if request.method == "POST":
        # In real scenario, verify signature here
        payment_id = request.POST.get('razorpay_payment_id')
        
        # Simulate Success
        Payment.objects.create(
            transaction_id=payment_id,
            payment_gateway="Razorpay",
            amount=0, # Retrieve actual amount in production
            status="Success"
        )
        
        return render(request, 'payments/success.html')
    
    return render(request, 'payments/failed.html')