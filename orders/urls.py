from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, update_order_status 

# Create a router and register our OrderViewSet
router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')
# router.register(r'neworder', NewOrderViewSet, basename='neworder')

urlpatterns = [
    path('', include(router.urls)),  # This route will be used for FitMaker orders
    path('<int:id>/update_status/', update_order_status, name='update_order_status'), 
    # path('update-status/<int:id>/', update_order_status2, name='update_order_status2'), 
]
