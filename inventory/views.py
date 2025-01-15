from rest_framework import status
from rest_framework import viewsets, filters, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import   InventoryItem, InventoryItemMovement
from fitMakers.models import FitMaker
from rest_framework.exceptions import NotFound
from .serializers import   InventoryItemSerializer, InventoryItemMovementSerializer
from decimal import Decimal

 
class InventoryPagination(pagination.PageNumberPagination):
    page_size = 5 # items per page
    page_size_query_param = 'page_size'
    max_page_size = 15

    
class InventoryItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InventoryItemSerializer
    pagination_class = InventoryPagination

    queryset = InventoryItem.objects.all()

    def get_queryset(self): 
        try:
            fitmaker = self.request.user.fitmaker
        except AttributeError:
            raise NotFound("FitMaker not found for the authenticated user.")

        queryset = InventoryItem.objects.filter(fitmaker=fitmaker)

        item_type = self.request.query_params.get('item_type', None)
        if item_type is not None:
            queryset = queryset.filter(item_type=item_type)

        return queryset







class InventoryItemMovementViewSet(viewsets.ModelViewSet): 
    queryset = InventoryItemMovement.objects.all()
    serializer_class = InventoryItemMovementSerializer
    pagination_class = InventoryPagination

    def get_queryset(self):
        """
        Get the list of inventory item movements filtered by the logged-in user's FitMaker.
        Only movements for the authenticated user's FitMaker will be returned.
        """
        # Get the authenticated user's FitMaker
        fitmaker = FitMaker.objects.filter(user=self.request.user).first()

        # If no FitMaker exists for the user, return an empty queryset
        if not fitmaker:
            return InventoryItemMovement.objects.none()

        # Filter InventoryItemMovements by the logged-in user's FitMaker
        queryset = InventoryItemMovement.objects.filter(inventory_item__fitmaker=fitmaker)

        # Additional filters based on query parameters (optional)
        inventory_item_id = self.request.query_params.get('inventory_item', None)
        category = self.request.query_params.get('category', None)

        if inventory_item_id is not None:
            queryset = queryset.filter(inventory_item_id=inventory_item_id)

        if category is not None:
            queryset = queryset.filter(inventory_item__category__icontains=category)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of an inventory item movement. Ensure the item belongs to the logged-in user's FitMaker.
        """
        # Get the FitMaker for the authenticated user
        fitmaker = FitMaker.objects.filter(user=request.user).first()

        if not fitmaker:
            return Response({"detail": "FitMaker not found."}, status=status.HTTP_400_BAD_REQUEST)

        inventory_item_id = request.data.get('inventory_item')
        quantity = request.data.get('quantity')
        movement_type = request.data.get('movement_type')
        description = request.data.get('description', '')

        # Validate quantity
        try:
            quantity = int(quantity)
        except ValueError:
            return Response({"detail": "'quantity' must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Find the inventory item, ensuring it belongs to the logged-in user's fitmaker
        inventory_item = InventoryItem.objects.filter(id=inventory_item_id, fitmaker=fitmaker).first()

        if not inventory_item:
            return Response({"detail": "Inventory item not found or doesn't belong to the authenticated user."}, status=status.HTTP_404_NOT_FOUND)

        # Handle the movement and ensure stock is updated correctly
        try:
            movement = InventoryItemMovement.create_movement(
                fitmaker=fitmaker,  # Pass the fitmaker here
                inventory_item=inventory_item,
                quantity=quantity,
                movement_type=movement_type,
                description=description
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Return the updated stock details after successful movement
        return Response({
            "detail": f"Stock updated for {inventory_item.name}. New stock: {inventory_item.stock}",
            "movement": self.get_serializer(movement).data
        })


 