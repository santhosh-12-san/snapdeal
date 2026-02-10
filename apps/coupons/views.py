from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from .models import Coupon

def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        
        try:
            # Check if coupon exists and is active
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            
            # Check if expired
            if coupon.valid_to < timezone.now():
                messages.error(request, "This coupon has expired.")
            else:
                # Save coupon ID to session (Logic handled in Cart View)
                request.session['coupon_id'] = coupon.id
                messages.success(request, f"Coupon '{code}' Applied! You saved Rs. {coupon.discount_amount}")
            
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid Coupon Code")
            
    return redirect('cart:view_cart')

def remove_coupon(request):
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
        messages.info(request, "Coupon Removed")
    return redirect('cart:view_cart')