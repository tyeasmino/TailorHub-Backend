from rest_framework import serializers, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer
from inventory.models import InventoryItem
from measurements.models import DressType
from fitFinders.models import FitFinder
from fitMakers.models import FitMaker
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet): 
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user   

        if hasattr(user, 'fitmaker'):   
            fit_maker = user.fitmaker   
            return Order.objects.filter(fit_maker=fit_maker)   
        
        if hasattr(user, 'fitfinder'):   
            fit_finder = user.fitfinder  
            return Order.objects.filter(fit_finder=fit_finder)   

        return Order.objects.none()  



    def create(self, request, *args, **kwargs):
        fabric_id = request.data.get('fabric')  # fabric ID from the frontend
        dress_id = request.data.get('dress')  # dress ID from the frontend
        fit_maker_id = request.data.get('fit_maker')  # selected fitmaker ID
        fit_finder = request.user.fitfinder  # Get the FitFinder based on the current logged-in user

        try:
            # Retrieve the fabric and dress from the inventory
            fabric = InventoryItem.objects.get(id=fabric_id, item_type='Fabric')
            dress = DressType.objects.get(id=dress_id)  # Assuming dress is also in InventoryItem
            fit_maker = FitMaker.objects.get(id=fit_maker_id)
        except InventoryItem.DoesNotExist:
            return Response({"detail": "Fabric not found."}, status=400)
        except DressType.DoesNotExist:
            return Response({"detail": "Dress not found."}, status=400)
        except FitMaker.DoesNotExist:
            return Response({"detail": "FitMaker not found."}, status=400)

        # Create the order with the selected fabric, dress, and fit_maker
        order = Order.objects.create(
            fit_finder=fit_finder,
            fit_maker=fit_maker,
            fabric=fabric,
            dress=dress,
        )

        return Response(OrderSerializer(order).data, status=201)
    

@api_view(['PATCH'])
def update_order_status(request, order_id):
    try:
        # Retrieve the order using the order_id
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the 'order_status' is present in the request data
    if 'order_status' not in request.data:
        return Response({"detail": "Order status is required."}, status=status.HTTP_400_BAD_REQUEST)

    new_status = request.data['order_status']
    
    # Validate that the new status is one of the valid choices
    if new_status not in ['Processing', 'Completed', 'Delivered']:
        return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    # Handle the "Completed" status update
    if new_status == 'Completed':
        fabric = order.fabric  # Get the fabric for this order
        
        # Check if the fabric stock is available
        if fabric.stock <= 0:
            return Response({"detail": "Insufficient fabric stock to complete the order."}, status=status.HTTP_400_BAD_REQUEST)
        
        # If stock is sufficient, reduce the fabric stock by 1
        fabric.stock -= 1  # Decrease fabric stock by 1
        fabric.save()  # Save the updated fabric stock

    # Update the order status
    order.order_status = new_status
    order.save()  # Save the updated order

    # Return a success response
    return Response({"detail": f"Order status updated to {new_status}."}, status=status.HTTP_200_OK)
