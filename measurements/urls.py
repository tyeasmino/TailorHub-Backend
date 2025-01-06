from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DressTypeViewSet, DressMeasurementViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'dress_category', DressTypeViewSet)
router.register(r'dress_measurements', DressMeasurementViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
