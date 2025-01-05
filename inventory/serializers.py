from rest_framework import serializers
from . import models




class ToolsInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ToolsInventory
        fields = '__all__' 


class ToolsInventoryMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ToolsInventoryMovement
        fields = '__all__'


    def validate(self, data):
        if data['movement_type'] == 'Use' and data['quantity'] > data['tool'].stock:
            raise serializers.ValidationError("Not enough stock available to use.")
        return data
    

