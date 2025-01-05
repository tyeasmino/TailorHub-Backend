from rest_framework import serializers
from . import models


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'


class FitMakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FitMaker
        fields = '__all__'
    
    def create(self, validated_data):
        image_url = validated_data.pop('image', None) 

        fit_maker = FitMaker.objects.create(**validated_data)
        if image_url:
            fit_maker.image = image_url 
            fit_maker.save()
        return fit_maker     