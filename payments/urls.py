from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our OrderViewSet
# router = DefaultRouter()
# router.register(r'', views.payment, basename='payment1')

urlpatterns = [
    # path('', include(router.urls)),  # This route will be used for FitMaker orders
    path('', views.payment, name='payment'), 
    path('goback', views.goback, name='goback'), 
    path('gohome', views.gohome, name='gohome'), 
]
