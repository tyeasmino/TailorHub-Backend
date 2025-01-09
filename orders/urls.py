from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, update_order_status, mock_payment_process

# Create a router and register our OrderViewSet
router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),  # This route will be used for FitMaker orders
    path('<int:id>/update_status/', update_order_status, name='update_order_status'),
    path('<int:id>/mock_payment/', mock_payment_process, name='mock_payment_process'),
]
