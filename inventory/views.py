from rest_framework import status
from rest_framework import viewsets, filters, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import   InventoryItem, InventoryItemMovement
from fitMakers.models import FitMaker
from rest_framework.exceptions import NotFound
from .serializers import   InventoryItemSerializer, InventoryItemMovementSerializer
from decimal import Decimal
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


class InventoryPagination(pagination.PageNumberPagination):
    page_size = 12 # items per page
    page_size_query_param = 'page_size'
    max_page_size = 25



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
        


class InventoryAllItems(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    pagination_class = InventoryPagination
    queryset = InventoryItem.objects.all()

    def get_queryset(self): 
        # Start by getting all inventory items
        queryset = InventoryItem.objects.all()

        # First, filter by "Fabric" and "Dress" item_type
        queryset = queryset.filter(item_type__in=["Fabric", "Dress"])

        # If an 'item_type' query param is provided, apply additional filtering
        item_type_param = self.request.query_params.get('item_type', None)
        if item_type_param:
            queryset = queryset.filter(item_type=item_type_param)
        
        is_featured_param = self.request.query_params.get('is_featured', None)
        if is_featured_param is not None:
            # Convert 'is_featured' to a boolean (it should be either 'true' or 'false')
            queryset = queryset.filter(is_featured=is_featured_param.lower() == 'true')

        is_upcoming_param = self.request.query_params.get('is_upcoming', None)
        if is_upcoming_param is not None:
            # Convert 'is_featured' to a boolean (it should be either 'true' or 'false')
            queryset = queryset.filter(is_upcoming=is_upcoming_param.lower() == 'true')

        return queryset





class InventoryItemMovementViewSet(viewsets.ModelViewSet): 
    queryset = InventoryItemMovement.objects.all()
    serializer_class = InventoryItemMovementSerializer
    pagination_class = InventoryPagination

    def get_queryset(self):
        fitmaker = FitMaker.objects.filter(user=self.request.user).first()

        if not fitmaker:
            return InventoryItemMovement.objects.none()

        queryset = InventoryItemMovement.objects.filter(inventory_item__fitmaker=fitmaker)

        inventory_item_id = self.request.query_params.get('inventory_item', None)
        category = self.request.query_params.get('category', None)

        if inventory_item_id is not None:
            queryset = queryset.filter(inventory_item_id=inventory_item_id)

        if category is not None:
            queryset = queryset.filter(inventory_item__category__icontains=category)

        return queryset

    def create(self, request, *args, **kwargs):
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


