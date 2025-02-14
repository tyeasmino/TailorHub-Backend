from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, update_order_status, CartListViewSet, add_to_cart, view_cart

# Create a router and register our OrderViewSet
router = DefaultRouter()
router.register(r'myorder', OrderViewSet, basename='order')
router.register(r'mycart', CartListViewSet, basename='cart')
# router.register(r'neworder', NewOrderViewSet, basename='neworder')

urlpatterns = [
    path('', include(router.urls)),  # This route will be used for FitMaker orders
    path('<int:id>/update_status/', update_order_status, name='update_order_status'), 
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
]
