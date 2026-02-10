from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from apps.products.models import Product
from apps.orders.models import Cart, CartItem  # <--- THIS IS CORRECT

@login_required
def view_wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist/list.html', {'items': items})

@login_required
def toggle_wishlist(request, product_id):
    """
    If item is in wishlist -> Remove it.
    If item is NOT in wishlist -> Add it.
    """
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.info(request, "Removed from Shortlist")
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, "Added to Shortlist")
    
    # Redirect back to the same page user was on
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def move_to_cart(request, product_id):
    """Action: Move item from Wishlist -> Cart"""
    product = get_object_or_404(Product, id=product_id)
    
    # 1. Add to Cart
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
        
    # 2. Remove from Wishlist
    Wishlist.objects.filter(user=request.user, product=product).delete()
    
    messages.success(request, "Moved to Cart")
    return redirect('cart:view_cart')