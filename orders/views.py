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



# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

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
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the status is being updated to 'Completed'
    if 'order_status' in request.data and request.data['order_status'] == 'Completed':
        fabric = order.fabric  # Get the fabric for this order
        if fabric.stock <= 0:  # Check if the fabric stock is available
            return Response({"detail": "Insufficient fabric stock to complete the order."}, status=status.HTTP_400_BAD_REQUEST)

    # If the new status is valid, update it
    if 'order_status' in request.data:
        new_status = request.data['order_status']
        if new_status not in ['Processing', 'Completed', 'Delivered']:
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the order status
        order.order_status = new_status

        # If the order is marked as completed, inventory will automatically update due to the save method
        if new_status == 'Completed':
            order.save()

        return Response({"detail": f"Order status updated to {new_status}."}, status=status.HTTP_200_OK)

    return Response({"detail": "Order status is required."}, status=status.HTTP_400_BAD_REQUEST)

