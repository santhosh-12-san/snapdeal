

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import JWT Views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

      # Connect all our apps
    path('', include('apps.core.urls')),           # Homepage
    path('users/', include('apps.users.urls')),
    path('shop/', include('apps.products.urls')),
    
    path('orders/', include('apps.orders.urls')),
    path('wishlist/', include('apps.wishlist.urls')),
    path('coupons/', include('apps.coupons.urls')),
    path('search/', include('apps.search.urls')),
    path('payments/', include('apps.payments.urls')),
    path('sell/', include('apps.vendors.urls')),
    
    
    # --- JWT AUTHENTICATION ENDPOINTS ---
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Login (Get Token)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresh Token
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)