from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'fit-makers', views.FitMakerViewSet) 
router.register(r'categories', views.CategoryViewSet)  # Register Category
router.register(r'dresses', views.DressViewSet)  # Register Dress
router.register(r'dress-ratings', views.DressRatingViewSet)  # Register Dress Ratings

urlpatterns = [
    path('', include(router.urls)),
    path('deposit/', views.DepositFundsView.as_view(), name='deposit-funds'),
    path('update-best-seller/', views.UpdateBestSellerView.as_view(), name='update_best_seller'),
    path('dresses/<int:pk>/', views.DressDetailView.as_view(), name='dress-detail'),
]
