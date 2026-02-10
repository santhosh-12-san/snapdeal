from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vendor
from apps.products.models import Product, Category

@login_required
def vendor_dashboard(request):
    # 1. Check if user is a registered vendor
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        # If not a vendor, redirect to registration page (you can build this later)
        messages.warning(request, "You need to register as a seller first.")
        return redirect('home')

    # 2. Get all products sold by this vendor
    products = Product.objects.filter(vendor=vendor).order_by('-created_at')
    
    context = {
        'vendor': vendor,
        'products': products,
        'total_sales': 0, # Placeholder for future sales logic
    }
    return render(request, 'vendors/dashboard.html', context)

@login_required
def add_product(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        original_price = request.POST.get('original_price')
        discounted_price = request.POST.get('discounted_price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        image = request.FILES.get('image') # Requires <form enctype="multipart/form-data">

        # Save to DB
        Product.objects.create(
            vendor=vendor,
            category_id=category_id,
            name=name,
            original_price=original_price,
            discounted_price=discounted_price,
            stock=stock,
            description=description,
            thumbnail=image,
            is_active=True
        )
        messages.success(request, "Product Added Successfully!")
        return redirect('vendors:dashboard')

    # GET Request: Show Form
    categories = Category.objects.all()
    return render(request, 'vendors/add_product.html', {'categories': categories})