from rest_framework import serializers
from .models import Order 




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



    


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['item', 'quantity', 'price', 'item_total_price']

#     # Optionally you could validate price and quantity
#     def validate(self, attrs):
#         if attrs['quantity'] <= 0:
#             raise serializers.ValidationError("Quantity must be greater than zero.")
#         return attrs


# class NewOrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)  # Nested order items
#     total_bill = serializers.SerializerMethodField()

#     class Meta:
#         model = NewOrder
#         fields = ['order_id', 'fit_finder', 'fit_maker', 'total_bill', 'items', 'order_status', 'is_paid', 'created_at', 'updated_at']

#     def get_total_bill(self, obj):
#         # Calculate total bill by summing item total prices
#         return sum([item.item_total_price for item in obj.items.all()])
