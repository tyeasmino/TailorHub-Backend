from rest_framework import serializers, viewsets, pagination
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
class OrderPagination(pagination.PageNumberPagination):
    page_size = 5 # items per page
    page_size_query_param = 'page_size'
    max_page_size = 15


class OrderViewSet(viewsets.ModelViewSet): 
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination

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
def update_order_status(request, id):  # Use `id` here
    try:
        # Retrieve the order by primary key (id)
        order = Order.objects.get(id=id)  # Use id for primary key lookup
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    # Debugging prints to check if the order is being retrieved correctly
    print(f"Order ID: {order.id}")  # Print the order ID (primary key)
    
    # Retrieve fabric and fitmaker related to this order
    fabric = order.fabric  # Access fabric from the order
    fitmaker = order.fit_maker  # Access fit_maker from the order

    
    # Ensure 'order_status' is in the request data
    if 'order_status' not in request.data:
        return Response({"detail": "Order status is required."}, status=status.HTTP_400_BAD_REQUEST)

    new_status = request.data['order_status']
    
    # Validate that the new status is one of the valid choices
    if new_status not in ['Processing', 'Completed', 'Delivered']:
        return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    # Update the order status and handle stock reduction for "Completed"
    if new_status == 'Completed':
        # Ensure fabric and fitmaker are properly accessed before the logic begins
        # Check if the fabric stock is available
        if fabric.stock <= 0:
            return Response({"detail": "Insufficient fabric stock to complete the order."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the fabric is in the FitMaker's inventory and update stock
        fitmaker_inventory_fabric = InventoryItem.objects.filter(
            fitmaker=fitmaker, 
            item_type='Fabric', 
            id=fabric.id
        ).first()

        if fitmaker_inventory_fabric:
            if fitmaker_inventory_fabric.stock > 0:
                fitmaker_inventory_fabric.stock -= 1  # Decrease fabric stock by 1
                fitmaker_inventory_fabric.save()  # Save the updated fabric stock
            else:
                return Response({"detail": "FitMaker's fabric stock is insufficient to complete the order."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Fabric not found in FitMaker's inventory."}, status=status.HTTP_400_BAD_REQUEST)

    # If status is not 'Completed', just update the order status
    order.order_status = new_status
    order.save()  # Save the updated order

    # Return a success response
    return Response({"detail": f"Order status updated to {new_status}."}, status=status.HTTP_200_OK)




@api_view(['POST'])
def mock_payment_process(request, id):
    try:
        # Retrieve the order using the id
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    # Simulate a payment response (e.g., randomly choose success or failure)
    import random
    payment_successful = random.choice([True, False])

    if payment_successful:
        # Mark the order as paid and delivered
        order.is_paid = True
        order.order_status = 'Delivered'
        order.save()
        return Response({"detail": "Payment successful, order status updated to 'Delivered'."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Payment failed, please try again."}, status=status.HTTP_400_BAD_REQUEST)