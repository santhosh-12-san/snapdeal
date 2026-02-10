from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Category, Review

def product_detail(request, slug):
    # 1. Get the Product
    product = get_object_or_404(Product, slug=slug)
    
    # 2. Get Related Data
    images = product.images.all()
    sizes = product.sizes.filter(stock__gt=0)
    
    # 3. Calculate Discount Percentage
    discount = product.discount_percentage

    # 4. Get Reviews
    reviews = product.reviews.all().order_by('-created_at')
    avg_rating = product.rating

    # 5. Get Similar Products
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    attributes = product.attributes.all()

    context = {
        'product': product,
        'images': images,
        'sizes': sizes,
        'discount': discount,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'similar_products': similar_products,
        'attributes': attributes,
    }
    
    return render(request, 'products/detail.html', context)


def category_list(request, slug):
    """This was the missing function causing the error"""
    category = get_object_or_404(Category, slug=slug)
    # Get all products in this category
    products = Product.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'products/list.html', context)

# API to check if the product can be delivered to a pincode
def check_pincode(request):
    is_available = False
    delivery_date = "N/A"
    message = "Not available in your area"

    if request.method == "GET":
        pincode = request.GET.get('pincode')
        
        if pincode and (pincode.startswith('11') or pincode.startswith('56') or pincode == '500001'):
            is_available = True
            delivery_date = "Delivery by 5 Days"
            message = delivery_date

    return JsonResponse({
        'available': is_available,
        'message': message
    })