from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToolsInventoryViewSet, ToolsInventoryMovementViewSet, InventoryItemViewSet, InventoryItemMovementViewSet

router = DefaultRouter()
# router.register(r'tools', ToolsInventoryViewSet)
# router.register(r'tools_movements', ToolsInventoryMovementViewSet)


router.register(r'items', InventoryItemViewSet, basename='inventory-item')
router.register(r'items_movements', InventoryItemMovementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
