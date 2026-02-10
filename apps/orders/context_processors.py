from .models import Cart

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        # 1. Logged-in User
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            # Sum up the quantities of all items
            count = sum(item.quantity for item in cart.items.all())
    else:
        # 2. Guest User (Session based)
        session_id = request.session.session_key
        if session_id:
            cart = Cart.objects.filter(session_id=session_id).first()
            if cart:
                count = sum(item.quantity for item in cart.items.all())

    # This makes {{ cart_count }} available in ALL templates
    return {'cart_count': count}