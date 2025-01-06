from rest_framework import serializers
from .models import DressType, DressMeasurement
from fitFinders.serializers import FitFinderSerializer

class DressTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DressType
        fields = '__all__'

class DressMeasurementSerializer(serializers.ModelSerializer):
    # fit_finder = FitFinderSerializer()  # Include the fit_finder in the serializer
    
    class Meta:
        model = DressMeasurement
        fields = '__all__'

    def validate(self, data):
        # Ensure that the fields are valid for the selected dress type
        dress_measurement = DressMeasurement(**data)  # Create instance of DressMeasurement with provided data
        if not dress_measurement.is_valid_for_dress_type():
            raise serializers.ValidationError("Missing required measurements for this dress type.")
        return data