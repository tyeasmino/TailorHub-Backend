from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'fit-makers', views.FitMakerViewSet) 


urlpatterns = [
    path('', include(router.urls)),
    path('deposit/', views.DepositFundsView.as_view(), name='deposit-funds'),
]
