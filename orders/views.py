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























# class NewOrderViewSet(viewsets.ModelViewSet):
#     serializer_class = NewOrderSerializer  # Use NewOrderSerializer here
#     permission_classes = [IsAuthenticated]
#     pagination_class = OrderPagination

#     def get_queryset(self):
#         user = self.request.user

#         if hasattr(user, 'fitmaker'):
#             fit_maker = user.fitmaker
#             return NewOrder.objects.filter(fit_maker=fit_maker)

#         if hasattr(user, 'fitfinder'):
#             fit_finder = user.fitfinder
#             return NewOrder.objects.filter(fit_finder=fit_finder)

#         return NewOrder.objects.none()

#     def create(self, request, *args, **kwargs):
#         fabric_ids = request.data.get('fabrics', [])  # List of fabric IDs
#         fit_maker_id = request.data.get('fit_maker')  # FitMaker ID
#         fit_finder = request.user.fitfinder  # FitFinder based on logged-in user

#         try:
#             # Retrieve fabrics from the inventory
#             fabrics = InventoryItem.objects.filter(id__in=fabric_ids, item_type='Fabric')
#             fit_maker = FitMaker.objects.get(id=fit_maker_id)
#         except InventoryItem.DoesNotExist:
#             return Response({"detail": "Some fabrics not found."}, status=400)
#         except FitMaker.DoesNotExist:
#             return Response({"detail": "FitMaker not found."}, status=400)

#         # Create the NewOrder object
#         new_order = NewOrder.objects.create(
#             fit_finder=fit_finder,
#             fit_maker=fit_maker,
#         )

#         total_bill = 0
#         order_items = []

#         for fabric in fabrics:
#             price = fabric.base_price  # Set price for fabric
#             # Create an OrderItem for each fabric
#             order_item = OrderItem.objects.create(
#                 order=new_order,
#                 item=fabric,
#                 quantity=1,  # You can customize quantity
#                 price=price
#             )
#             order_items.append(order_item)
#             total_bill += price

#         # Update the total_bill in the NewOrder object
#         new_order.total_bill = total_bill
#         new_order.save()

#         # Serialize and return the response
#         return Response(NewOrderSerializer(new_order).data, status=201)


# @api_view(['PATCH'])
# def update_order_status2(request, id):
#     try:
#         # Retrieve the NewOrder by ID
#         order = NewOrder.objects.get(id=id)
#     except NewOrder.DoesNotExist:
#         return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

#     # Ensure 'order_status' is provided in the request data
#     if 'order_status' not in request.data:
#         return Response({"detail": "Order status is required."}, status=status.HTTP_400_BAD_REQUEST)

#     new_status = request.data['order_status']
    
#     # Validate status
#     if new_status not in ['Processing', 'Completed', 'Delivered']:
#         return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

#     # Handle stock reduction for "Completed" status
#     if new_status == 'Completed':
#         # Decrease fabric stock for each item in the order
#         for order_item in order.items.all():
#             fabric = order_item.item  # Access the fabric
#             if fabric.stock <= 0:
#                 return Response({"detail": f"Insufficient fabric stock for {fabric.name}."}, status=status.HTTP_400_BAD_REQUEST)
            
#             # Reduce the fabric stock in the inventory
#             fabric.stock -= 1
#             fabric.save()

#     # Update order status and save
#     order.order_status = new_status
#     order.save()

#     return Response({"detail": f"Order status updated to {new_status}."}, status=status.HTTP_200_OK)



# class CreateNewOrder(APIView):
#     def post(self, request, *args, **kwargs):
#         fit_finder = request.user.fitfinder
#         fit_maker_id = request.data.get('fit_maker')
#         item_data = request.data.get('items', [])  # Assuming items is a list of item data
        
#         try:
#             # Retrieve the FitMaker object
#             fit_maker = FitMaker.objects.get(id=fit_maker_id)
            
#             # Create a new NewOrder instance
#             new_order = NewOrder.objects.create(
#                 fit_finder=fit_finder,
#                 fit_maker=fit_maker,
#             )

#             # Create OrderItems and associate them with the NewOrder
#             for item in item_data:
#                 item_instance = InventoryItem.objects.get(id=item['item_id'])
#                 order_item = OrderItem.objects.create(
#                     item=item_instance,
#                     quantity=item['quantity'],
#                     price=item_instance.price,
#                     order=new_order
#                 )
#                 new_order.items.add(order_item)

#             # Optionally, update total bill or other fields on the NewOrder
#             new_order.total_bill = sum([oi.item_total_price for oi in new_order.items.all()])
#             new_order.save()

#             return Response(NewOrderSerializer(new_order).data, status=status.HTTP_201_CREATED)
        
#         except FitMaker.DoesNotExist:
#             return Response({"detail": "FitMaker not found."}, status=status.HTTP_400_BAD_REQUEST)
#         except InventoryItem.DoesNotExist:
#             return Response({"detail": "Item not found."}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)