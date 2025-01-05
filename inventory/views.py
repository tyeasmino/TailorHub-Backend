from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import ToolsInventory, ToolsInventoryMovement
from .serializers import ToolsInventorySerializer, ToolsInventoryMovementSerializer

class ToolsInventoryViewSet(viewsets.ModelViewSet):
    queryset = ToolsInventory.objects.all()
    serializer_class = ToolsInventorySerializer

    # Custom action to update stock
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        tool = self.get_object()
        
        
        quantity = request.data.get('quantity')
        movement_type = request.data.get('movement_type')
        
        if quantity is None or movement_type is None:
            return Response({"detail": "Both 'quantity' and 'movement_type' are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quantity = int(quantity)
        except ValueError:
            return Response({"detail": "'quantity' must be an integer."}, status=status.HTTP_400_BAD_REQUEST)


        if movement_type == 'Add':
            tool.update_stock(quantity)
            InventoryMovement.objects.create(
                tool=tool,
                quantity=quantity,
                movement_type="Add",
                description=request.data.get('description', '')
            )
        elif movement_type == 'Use':
            if quantity > tool.stock:
                return Response({"detail": "Not enough stock available to use."}, status=status.HTTP_400_BAD_REQUEST)
            tool.update_stock(-quantity)
            InventoryMovement.objects.create(
                tool=tool,
                quantity=-quantity,
                movement_type="Use",
                description=request.data.get('description', '')
            )
        else:
            return Response({"detail": "Invalid 'movement_type'. Must be 'Add' or 'Use'."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": f"Stock updated. New stock for {tool.name}: {tool.stock}"})

class ToolsInventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = ToolsInventoryMovement.objects.all()  
    serializer_class = ToolsInventoryMovementSerializer
