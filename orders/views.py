from rest_framework import serializers, viewsets, pagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from .models import Order, CartList
from .serializers import OrderSerializer, CartListSerializer
from inventory.models import InventoryItem
from measurements.models import DressType
from fitFinders.models import FitFinder
from fitMakers.models import FitMaker
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required  


# Create your views here.
# Create a viewset to handle CartList actions
def perform_create(self, serializer):
    # Automatically save the fit_finder as the logged-in user
    serializer.save(fit_finder=self.request.user.fitfinder)


class CartListViewSet(viewsets.ModelViewSet):
    serializer_class = CartListSerializer

    def get_queryset(self):
        return CartList.objects.filter(fit_finder=self.request.user.fitfinder)

    def perform_create(self, serializer):
        serializer.save()



@api_view(['POST'])
def add_to_cart(request):
    # Assuming you're passing the necessary data in the request
    user = request.user  # This will give you the logged-in user
    fit_finder = user.fitFinder
    fit_maker = user.fitMaker  # Assuming that the user has a fitMaker associated with them

    if not fit_finder:
        return Response({'error': 'FitFinder not associated with user'}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    fabric_or_dress_id = data.get('fabric_or_dress')
    tailor_service_id = data.get('tailorService')
    quantity = data.get('fabric_or_dress_quantity', 1)

    # Fetch the related objects (inventory item and dress type)
    try:
        fabric_or_dress = InventoryItem.objects.get(id=fabric_or_dress_id)
        tailor_service = DressType.objects.get(id=tailor_service_id) if tailor_service_id else None
    except InventoryItem.DoesNotExist:
        return Response({'error': 'Fabric or Dress item not found'}, status=status.HTTP_400_BAD_REQUEST)
    except DressType.DoesNotExist:
        return Response({'error': 'Tailor service not found'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the cart item
    cart_item = CartList.objects.create(
        fit_finder=fit_finder,
        fabric_or_dress=fabric_or_dress,
        fabric_or_dress_quantity=quantity,
        tailorService=tailor_service,
        fit_maker=fit_maker  # Associate fitMaker
    )

    # You can serialize the response here if needed
    return Response(CartListSerializer(cart_item).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_order(request):
    user = request.user
    fit_finder = user.fitFinder
    fit_maker = user.fitMaker

    if not fit_finder:
        return Response({'error': 'FitFinder not associated with user'}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    fabric_or_dress_id = data.get('fabric_OR_dress')
    tailor_service_id = data.get('tailorService')
    quantity = data.get('fabric_OR_dress_quantity', 1)

    # Fetch the related objects
    try:
        fabric_or_dress = InventoryItem.objects.get(id=fabric_or_dress_id)
        tailor_service = DressType.objects.get(id=tailor_service_id) if tailor_service_id else None
    except InventoryItem.DoesNotExist:
        return Response({'error': 'Fabric or Dress item not found'}, status=status.HTTP_400_BAD_REQUEST)
    except DressType.DoesNotExist:
        return Response({'error': 'Tailor service not found'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the order
    order = Order.objects.create(
        fit_finder=fit_finder,
        fit_maker=fit_maker,
        fabric_OR_dress=fabric_or_dress,
        fabric_OR_dress_quantity=quantity,
        tailorService=tailor_service,
    )

    # Return the serialized order data
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    

@api_view(['GET'])
@login_required
def view_cart(request):
    cart_items = CartList.objects.filter(fit_finder=request.user.fitfinder, purchased=False)
    return Response(CartListSerializer(cart_items, many=True).data)


@api_view(['POST'])
@login_required
def create_order_from_cart(request):
    cart_items = CartList.objects.filter(fit_finder=request.user.fitfinder, purchased=False)
    
    if not cart_items.exists():
        return Response({"detail": "Your cart is empty."}, status=400)
    
    # Calculate total price
    total_price = sum([item.get_total() for item in cart_items])
    
    # Create Order
    order = Order.objects.create(
        fit_finder=request.user.fitfinder,
        total_bill=total_price,
        is_paid=False,  # or True if already paid
        order_status='Processing',
    )

    for cart_item in cart_items:
        # Add cart items to the order
        OrderItem.objects.create(
            order=order,
            fabric_or_dress=cart_item.fabric_or_dress,
            fabric_or_dress_quantity=cart_item.fabric_or_dress_quantity,
            tailorService=cart_item.tailorService,
            fit_maker=cart_item.fit_maker,
        )

        # Mark cart item as purchased
        cart_item.purchased = True
        cart_item.save()

    return Response(OrderSerializer(order).data, status=201)









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
