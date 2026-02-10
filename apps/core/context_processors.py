

# 👇 NOTICE: We are importing from 'apps.products.models', NOT '.models'
from apps.products.models import Category 

def categories_processor(request):
    # Fetch categories where parent is Empty (None)
    main_categories = Category.objects.filter(parent=None)
    
    
    
    return {'main_categories': main_categories}