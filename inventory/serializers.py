from rest_framework import serializers
from . import models



 
class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InventoryItem
        fields = '__all__'

    def create(self, validated_data): 
        image_url = validated_data.pop('image', None) 
        
        inventory_item = models.InventoryItem.objects.create(**validated_data)
        if image_url:
            inventory_item.image = image_url
            inventory_item.save()

        return inventory_item


class InventoryItemMovementSerializer(serializers.ModelSerializer):
    inventory_item_name = serializers.CharField(source='inventory_item.name')

    class Meta:
        model = models.InventoryItemMovement
        fields = ['id', 'inventory_item_name', 'quantity', 'movement_type', 'date', 'description']

    def validate(self, data):
        # Validate quantity for "Use" movement
        if data['movement_type'] == 'Use' and data['quantity'] > data['inventory_item'].stock:
            raise serializers.ValidationError("Not enough stock available to use.")
        return data
