from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ToolsInventory, ToolsInventoryMovement, InventoryItem, InventoryItemMovement
from fitMakers.models import FitMaker
from rest_framework.exceptions import NotFound
from .serializers import ToolsInventorySerializer, ToolsInventoryMovementSerializer, InventoryItemSerializer, InventoryItemMovementSerializer
from decimal import Decimal



class ToolsInventoryViewSet(viewsets.ModelViewSet):
    queryset = ToolsInventory.objects.all()
    serializer_class = ToolsInventorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        fitmaker_id = self.request.query_params.get('fitmaker', None)
        category = self.request.query_params.get('category', None)

        # Filter by fitmaker if provided
        if fitmaker_id is not None:
            queryset = queryset.filter(fitmaker_id=fitmaker_id)

        # Filter by category if provided
        if category is not None:
            queryset = queryset.filter(category__icontains=category)

        return queryset

    def create(self, request, *args, **kwargs):
        # Extract tool data from the request
        name = request.data.get('name')
        color = request.data.get('color')
        category = request.data.get('category')
        condition = request.data.get('condition')
        supplier = request.data.get('supplier')
        fitmaker_id = request.data.get('fitmaker')

        # Find the FitMaker object based on the ID
        try:
            fitmaker = FitMaker.objects.get(id=fitmaker_id)
        except FitMaker.DoesNotExist:
            return Response({"detail": "FitMaker not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the tool already exists for this specific FitMaker
        existing_tool = ToolsInventory.objects.filter(
            name=name,
            color=color,
            category=category,
            condition=condition,
            supplier=supplier,
            fitmaker=fitmaker
        ).first()

        if existing_tool:
            return Response({
                "detail": f"Tool '{name}' already exists for this FitMaker. You can update the stock using tool movements."
            }, status=status.HTTP_400_BAD_REQUEST)

        # If the tool doesn't exist for this FitMaker, create a new tool
        tool = ToolsInventory.objects.create(
            name=name,
            color=color,
            category=category,
            condition=condition,
            supplier=supplier,
            fitmaker=fitmaker,
            stock=0  # Start with 0 stock
        )

        # Return the created tool's details
        return Response(self.get_serializer(tool).data, status=status.HTTP_201_CREATED)



class ToolsInventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = ToolsInventoryMovement.objects.all()  # Default queryset
    serializer_class = ToolsInventoryMovementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get the 'tool' query parameter from the request
        tool_id = self.request.query_params.get('tool', None)
        
        # If the 'tool' parameter is provided, filter the queryset by tool
        if tool_id is not None:
            queryset = queryset.filter(tool_id=tool_id)

        return queryset

    def create(self, request, *args, **kwargs):
        # Extract movement details from request
        tool_id = request.data.get('tool')
        quantity = request.data.get('quantity')
        movement_type = request.data.get('movement_type')
        description = request.data.get('description', '')

        # Validate quantity
        try:
            quantity = int(quantity)
        except ValueError:
            return Response({"detail": "'quantity' must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Find the tool
        tool = ToolsInventory.objects.filter(id=tool_id).first()
        if not tool:
            return Response({"detail": "Tool not found."}, status=status.HTTP_404_NOT_FOUND)

        # Handle "Add" or "Use" movement
        if movement_type == "Add":
            tool.stock += quantity  # Increase stock
        elif movement_type == "Use":
            if quantity > tool.stock:
                return Response({"detail": "Not enough stock available to use."}, status=status.HTTP_400_BAD_REQUEST)
            tool.stock -= quantity  # Decrease stock
        else:
            return Response({"detail": "Invalid 'movement_type'. Must be 'Add' or 'Use'."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated tool stock
        tool.save()

        # Create the movement entry (record the movement)
        movement = ToolsInventoryMovement.objects.create(
            tool=tool,
            quantity=quantity if movement_type == "Add" else -quantity,
            movement_type=movement_type,
            description=description
        )

        # Return the updated stock details
        return Response({
            "detail": f"Stock updated for tool {tool.name}. New stock: {tool.stock}",
            "movement": self.get_serializer(movement).data
        })

    
class InventoryItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InventoryItemSerializer

    # Define the default queryset
    queryset = InventoryItem.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the inventory items
        that are related to the currently authenticated user's FitMaker.
        """
        # Get the authenticated user's fitmaker
        try:
            fitmaker = self.request.user.fitmaker
        except AttributeError:
            raise NotFound("FitMaker not found for the authenticated user.")

        # Filter InventoryItems by the fitmaker of the authenticated user
        queryset = InventoryItem.objects.filter(fitmaker=fitmaker)

        # Additional filters based on query parameters
        item_type = self.request.query_params.get('item_type', None)
        if item_type is not None:
            queryset = queryset.filter(item_type=item_type)

        return queryset







class InventoryItemMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryItemMovement.objects.all()  # Default queryset
    serializer_class = InventoryItemMovementSerializer

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


 