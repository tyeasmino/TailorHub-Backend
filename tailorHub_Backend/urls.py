from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('contact_us/', include("contactUs.urls")),
    path('fitFinders/', include("fitFinders.urls")),
    path('fitMakers/', include("fitMakers.urls")), 
    path('inventory/', include("inventory.urls")), 
    # path('measurements/', include("measurements.urls")), 
    path('api-auth/', include("rest_framework.urls")),
    path('auth/', include("dj_rest_auth.urls")),
    path('auth/', include("django.contrib.auth.urls")), 
]
