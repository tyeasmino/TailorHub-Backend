from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'fit-finder', views.FitFinderViewSet, basename='fit-finder')
 
urlpatterns = [
    path('', include(router.urls)),
]
