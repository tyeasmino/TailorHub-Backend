from rest_framework import serializers
from .models import FitFinder


class FitFinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitFinder
        fields = '__all__'
    
    def create(self, validated_data):
        image_url = validated_data.pop('image', None) 

        fit_finder = FitFinder.objects.create(**validated_data)
        if image_url:
            fit_finder.image = image_url 
            fit_finder.save()
        return fit_finder     
