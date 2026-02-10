from django.contrib import admin
# FIX 1: Cleaned up imports (Removed duplicate Category import and fixed the space typo)
from .models import (
    Category, Product, ProductImage, 
    ProductSize, ProductColor, ProductSpecification, 
    ProductAttribute, Review
)

# --- INLINE MODELS ---
# These allow you to add images/sizes directly inside the Product page
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

# --- MAIN MODEL ADMINS ---
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    # FIX 2: Combined your two list_display lines into one perfect line
    list_display = ('name', 'selling_price', 'category', 'is_deal_of_day', 'is_new_arrival', 'stock')
    list_filter = ('category', 'is_deal_of_day', 'is_active', 'is_new_arrival')
    search_fields = ('name', 'category__name')
    
    # This adds the tabs to upload multiple images/sizes on the same page
    inlines = [ProductImageInline, ProductSizeInline, ProductColorInline, ProductAttributeInline]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')

# --- REGISTER EVERYTHING ---
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)

# It is perfectly fine to register this separately! 
# It lets you see a list of ALL attributes across ALL products in one place.
admin.site.register(ProductAttribute)