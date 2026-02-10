# apps/orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
import uuid
import razorpay
from .models import Order, OrderItem # Make sure these are imported
# Import Models
from .models import Cart, CartItem, Order, OrderItem
from apps.products.models import Product
from apps.users.models import Address



# --- HELPER: Get Cart ---
def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_id=request.session.session_key, defaults={'user': None})
    return cart

# --- 1. CART PAGE ---
def view_cart(request):
    cart = _get_cart(request)
    context = {'cart': cart, 'cart_items': cart.items.all(), 'total_price': cart.get_total_price()}
    return render(request, 'orders/cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('orders:view_cart')

def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    get_object_or_404(CartItem, id=item_id, cart=cart).delete()
    return redirect('orders:view_cart')

# --- 2. ADDRESS PAGE (Matches your Screenshot) ---
@login_required(login_url='/users/login/')
def checkout(request):
    cart = _get_cart(request)
    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        # User selected an address, go to Payment
        return redirect('orders:payment')

    context = {
        'addresses': addresses,
        'cart': cart,
        'cart_items': cart.items.all(),
        'total_price': cart.get_total_price()
    }
    return render(request, 'orders/checkout_address.html', context)

# --- 3. PAYMENT PAGE ---
@login_required
def payment(request):
    cart = _get_cart(request)
    total_price = cart.get_total_price()
    razorpay_amount = int(total_price * 100) 

    context = {
        'cart': cart,
        'total_price': total_price,
        'razorpay_amount': razorpay_amount,
        'razorpay_key': 'rzp_test_S6vcSahmsz2Zjt' # Your Real Key
    }
    return render(request, 'orders/payment.html', context)

# apps/orders/views.py

# ... (Keep your imports) ...


# ---# apps/orders/views.py (Partial Update - Scroll to bottom)

import uuid
from .models import Order, OrderItem, Address 
# Make sure OrderItem is imported!

# --- 1. PAYMENT SUCCESS (Fixed to match YOUR Model) ---
@csrf_exempt
def payment_success(request):
    """
    Saves the order using your EXISTING database fields.
    """
    cart = _get_cart(request)
    
    # Get Address from Session
    address_id = request.session.get('selected_address_id')
    if not address_id:
        # Fallback: Use the first address found
        address = Address.objects.filter(user=request.user).first()
    else:
        address = Address.objects.get(id=address_id)

    # 1. Create Order (Using 'total_amount' and 'payment_method')
    new_order = Order.objects.create(
        user=request.user,
        address=address,
        order_id=str(uuid.uuid4())[:8].upper(), # Generates "A1B2C3D4"
        
        # FIXED FIELDS HERE:
        total_amount=cart.get_total_price(), # Matches your model's 'total_amount'
        payment_method="Card",               # Matches your CHOICES ('Card', 'UPI', etc.)
        status="Placed"                      # Matches your STATUS_CHOICES
    )

    # 2. Move Items from Cart to Order
    for item in cart.items.all():
        OrderItem.objects.create(
            order=new_order,
            product=item.product,
            price=item.product.selling_price, # Using selling_price as per your Cart logic
            quantity=item.quantity
        )

    # 3. Clear Cart
    cart.items.all().delete()
    
    # 4. Redirect to Tracking
    return redirect('orders:track_order', order_id=new_order.order_id)


# --- 2. TRACKING VIEW ---
@login_required
def track_order(request, order_id):
    try:
        # Get the order belonging to this user
        order = Order.objects.get(order_id=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found")
        return redirect('core:home')

    context = {
        'order': order,
        'order_items': order.items.all()
    }
    return render(request, 'orders/track_order.html', context)


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


# apps/orders/views.py

@login_required
def my_orders(request):
    """
    Displays a list of all past orders for the logged-in user.
    """
    # Get all orders for this user, ordered by newest first
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'orders/my_orders.html', context)