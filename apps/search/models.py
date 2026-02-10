from django.db import models
from django.conf import settings
from apps.products.models import Category

class SearchHistory(models.Model):
    # Track who searched (User or Guest)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='search_history')
    session_key = models.CharField(max_length=40, null=True, blank=True) # Critical for tracking Guests (not logged in)
    
    # What did they search for?
    query = models.CharField(max_length=255)
    
    # Did they apply filters? (Don't lose this data!)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # e.g., Searched "Shoes" inside "Men's Fashion"
    
    # Analytics: How many results did they find?
    # (If this is 0, you know you need to stock this product!)
    results_count = models.PositiveIntegerField(default=0)
    
    # When did it happen?
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Meta data (Optional but good for analytics)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Search Histories"
        ordering = ['-created_at'] # Show latest searches first

    def __str__(self):
        return f"'{self.query}' by {self.user if self.user else 'Guest'}"

# [Optional] To store "Trending Searches" explicitly if you want to curate them manually
class TrendingSearch(models.Model):
    query = models.CharField(max_length=255)
    url_link = models.CharField(max_length=500, help_text="Link to the search results page")
    rank = models.PositiveIntegerField(default=1, help_text="Order of display (1 is top)")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.query