from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework import viewsets, pagination 
from . import models, serializers
from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class FitMakerPagination(pagination.PageNumberPagination):
    page_size = 5 # items per page
    page_size_query_param = 'page_size'
    max_page_size = 15

class FitMakerProfileViewSet(viewsets.ModelViewSet):
    queryset = models.FitMaker.objects.all()
    serializer_class = serializers.FitMakerSerializer
    pagination_class = FitMakerPagination

class FitMakerViewSet(viewsets.ModelViewSet):
    queryset = models.FitMaker.objects.all()
    serializer_class = serializers.FitMakerSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return SkillSeeker.objects.filter(user = self.request.user)
    

class DepositFundsView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can deposit funds

    def post(self, request, *args, **kwargs):
        # Get the amount to deposit from the request data
        amount = request.data.get('amount', None)
        
        if amount is None:
            return Response({"detail": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert the amount to a decimal (decimal.Decimal is better than float for currency)
            amount = Decimal(str(amount))  # Ensuring we convert it properly to a Decimal
            if amount <= 0:
                return Response({"detail": "Deposit amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"detail": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the FitMaker object associated with the authenticated user
        fitmaker = get_object_or_404(models.FitMaker, user=request.user)

        # Add the deposit amount to the FitMaker's balance
        fitmaker.balance += amount
        fitmaker.save()

        # Return the updated balance as a response
        return Response({"detail": f"Successfully deposited {amount}. New balance: {fitmaker.balance}"}, status=status.HTTP_200_OK)

    


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class DressViewSet(viewsets.ModelViewSet):
    queryset = models.Dress.objects.all()
    serializer_class = serializers.DressSerializer

    def get_queryset(self): 
        # Start with the base queryset
        queryset = models.Dress.objects.all()
        
        is_upcoming = self.request.query_params.get('is_upcoming', None)
        if is_upcoming is not None:
            queryset = queryset.filter(is_upcoming=is_upcoming.lower() == 'true')  # Convert to boolean
 
        is_featured = self.request.query_params.get('is_featured', None)
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')

        return queryset
 


class DressDetailView(APIView):
    def get(self, request, pk):
        try:
            # Fetch the dress by primary key (id)
            dress = Dress.objects.get(pk=pk)
            serializer = DressSerializer(dress)
            return Response(serializer.data)
        except Dress.DoesNotExist:
            # If dress is not found, return a 404
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)



class DressRatingViewSet(viewsets.ModelViewSet):
    queryset = models.DressRating.objects.all()
    serializer_class = serializers.DressRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optionally filter ratings for the authenticated user, if needed
        return models.DressRating.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Optionally handle custom logic for rating creation, such as checking for duplicate ratings
        user = self.request.user
        dress = serializer.validated_data['dress']
        
        # Prevent the user from rating the same dress multiple times
        if models.DressRating.objects.filter(user=user, dress=dress).exists():
            raise serializers.ValidationError("You have already rated this dress.")
        
        # Save the rating
        serializer.save(user=user)


class UpdateBestSellerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the dress ID from the request
        dress_id = request.data.get('dress_id', None)
        
        if not dress_id:
            return Response({"detail": "Dress ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        dress = get_object_or_404(models.Dress, id=dress_id)
        dress.update_best_seller_status()  # Call your method to update best-seller status

        return Response({"detail": f"Best-seller status updated for {dress.name}"}, status=status.HTTP_200_OK)
