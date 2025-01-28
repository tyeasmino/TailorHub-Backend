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
from rest_framework.views import APIView



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
        fabric_OR_dress_id = request.data.get('fabric_OR_dress')  # fabric ID from the frontend
        tailorService_id = request.data.get('tailorService')  # dress ID from the frontend
        fabric_OR_dress_quantity = request.data.get('fabric_OR_dress_quantity', 1)
        fit_maker_id = request.data.get('fit_maker')  # selected fitmaker ID
        fit_finder = request.user.fitfinder  # Get the FitFinder based on the current logged-in user

        try:
            # Retrieve the fabric and dress from the inventory
            fabric_OR_dress = InventoryItem.objects.get(id=fabric_OR_dress_id)
            tailorService = DressType.objects.get(id=tailorService_id) if tailorService_id else None   
            fit_maker = FitMaker.objects.get(id=fit_maker_id)
        except InventoryItem.DoesNotExist:
            return Response({"detail": "Fabric or Dress not found."}, status=400)
        except DressType.DoesNotExist:
            return Response({"detail": "Tailor Service not found."}, status=400)
        except FitMaker.DoesNotExist:
            return Response({"detail": "FitMaker not found."}, status=400)

        # Create the order with the selected fabric, dress, and fit_maker
        order = Order.objects.create(
            fit_finder=fit_finder,
            fit_maker=fit_maker,
            fabric_OR_dress=fabric_OR_dress,
            tailorService=tailorService,
            fabric_OR_dress_quantity=fabric_OR_dress_quantity,
        )

        return Response(OrderSerializer(order).data, status=201)
    


@api_view(['PATCH'])
def update_order_status(request, id):  
    try: 
        order = Order.objects.get(id=id)  
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    if 'order_status' not in request.data:
        return Response({"detail": "Order status is required."}, status=status.HTTP_400_BAD_REQUEST)

    new_status = request.data['order_status']
     
    if new_status not in ['Processing', 'Completed', 'Delivered']:
        return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
 
    if new_status == 'Completed': 
        fabric_or_dress = order.fabric_OR_dress
        
        if fabric_or_dress:
            if fabric_or_dress.stock >= order.fabric_OR_dress_quantity: 
                fabric_or_dress.stock -= order.fabric_OR_dress_quantity
                fabric_or_dress.save()
            else:
                return Response({"detail": "Insufficient stock to complete the order."}, status=status.HTTP_400_BAD_REQUEST)

    order.order_status = new_status
    order.save()   

    return Response({"detail": f"Order status updated to {new_status}."}, status=status.HTTP_200_OK)
