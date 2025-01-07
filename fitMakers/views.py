from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework import viewsets 
from . import models, serializers
from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


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