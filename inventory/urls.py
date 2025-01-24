from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, InventoryItemMovementViewSet, InventoryAllItems

router = DefaultRouter() 


router.register(r'items', InventoryItemViewSet, basename='inventory-item')
router.register(r'items_movements', InventoryItemMovementViewSet)
router.register(r'all_items', InventoryAllItems)


urlpatterns = [
    path('', include(router.urls)), 
]
