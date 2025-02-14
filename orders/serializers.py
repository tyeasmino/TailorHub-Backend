from rest_framework import serializers
from .models import Order, CartList


# Create a serializer to handle cart list data

    
class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartList
        fields = fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # Add related field names for better readability in the response
    fabric_OR_dress_name = serializers.CharField(source='fabric_OR_dress.name', read_only=True)
    tailorService_name = serializers.CharField(source='tailorService.name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'fabric_OR_dress_quantity', 'fabric_OR_dress_price', 
            'tailorService_price', 'total_bill', 'is_paid', 'created_at', 
            'order_status', 'fit_finder', 'fit_maker', 'fabric_OR_dress', 'tailorService',
            'fabric_OR_dress_name', 'tailorService_name'  # Add these fields to the response
        ]