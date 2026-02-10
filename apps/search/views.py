from django.shortcuts import render
from django.db.models import Q
from apps.products.models import Product
from .models import SearchHistory

def search_results(request):
    query = request.GET.get('q', '')
    products = []
    
    if query:
        # 1. Search Logic: Filter by Name, Description, or Category
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        )

        # 2. Analytics: Save Search History
        if request.user.is_authenticated:
            SearchHistory.objects.create(
                user=request.user,
                query=query,
                results_count=products.count()
            )
        else:
            # Log guest searches
            SearchHistory.objects.create(
                session_key=request.session.session_key,
                query=query,
                results_count=products.count()
            )

    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'search/results.html', context)