from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToolsInventoryViewSet, ToolsInventoryMovementViewSet

router = DefaultRouter()
router.register(r'tools', ToolsInventoryViewSet)
router.register(r'tools_movements', ToolsInventoryMovementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
