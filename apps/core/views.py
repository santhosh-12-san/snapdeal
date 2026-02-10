from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from apps.core.models import Banner
from apps.products.models import Product, Category, ProductImage, ProductSize, ProductColor, ProductSpecification # Import these explicitly

# --- HOME VIEW ---
def home(request):
    sliders = Banner.objects.filter(section='Main Slider', is_active=True).order_by('order')
    deals = Product.objects.filter(is_deal_of_day=True).order_by('-created_at')
    mid_banners = Banner.objects.filter(section='Mid Strip', is_active=True).order_by('order')
    new_arrivals = Product.objects.filter(is_new_arrival=True, is_active=True).order_by('-created_at')
    footer_banners = Banner.objects.filter(section='Footer', is_active=True).order_by('order')
    
    # Randomly pick 20 products for the explore section
    explore_products = Product.objects.filter(is_active=True).order_by('?')[:20]
    
    # Get main categories for the menu
    main_categories = Category.objects.filter(parent__isnull=True).prefetch_related(
        'children',
        'children__children'
    )

    context = {
        'sliders': sliders,
        'deals': deals,
        'mid_banners': mid_banners,
        'new_arrivals': new_arrivals,
        'footer_banners': footer_banners,
        'explore_products': explore_products,
        'main_categories': main_categories,
    }
    return render(request, 'core/home.html', context)


# --- CATEGORY PAGE (With Filters) ---
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_active=True)

    # Sorting Logic
    sort_by = request.GET.get('sort', 'popularity')
    if sort_by == 'price_low':
        products = products.order_by('selling_price')
    elif sort_by == 'price_high':
        products = products.order_by('-selling_price')
    elif sort_by == 'new':
        products = products.order_by('-created_at')
    
    # Price Filter Logic
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(selling_price__gte=min_price)
    if max_price:
        products = products.filter(selling_price__lte=max_price)

    context = {
        'category': category,
        'products': products,
        'product_count': products.count(),
    }
    return render(request, 'core/category_detail.html', context)


# --- SEARCH VIEW ---
def search(request):
    query = request.GET.get('q', '')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        )
    
    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'core/search.html', context)


# --- PRODUCT DETAIL VIEW (FIXED) ---
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # FIX: Fetch related items directly using the models instead of reverse relations
    # This prevents 'AttributeError' if the related_name isn't set perfectly
    try:
        images = ProductImage.objects.filter(product=product)
    except:
        images = []

    try:
        sizes = ProductSize.objects.filter(product=product)
    except:
        sizes = []

    try:
        colors = ProductColor.objects.filter(product=product)
    except:
        colors = []

    try:
        specs = ProductSpecification.objects.filter(product=product)
    except:
        specs = []
    
    context = {
        'product': product,
        'images': images,
        'sizes': sizes,
        'colors': colors,
        'specs': specs,
    }
    return render(request, 'core/product_detail.html', context)