from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

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
            fit_maker.image = image_url  # Save image URL if provided
            fit_maker.save()
        return fit_maker

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class DressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dress
        fields = '__all__'

    def create(self, validated_data): 
        image_url = validated_data.pop('image_url', None)  # Ensure field name matches model
        
        # Optionally generate the slug if not provided
        if 'slug' not in validated_data:
            validated_data['slug'] = validated_data['name'].lower().replace(" ", "-")  # Example slug logic
        
        dress = models.Dress.objects.create(**validated_data)
        
        if image_url:
            dress.image_url = image_url  # Save image URL if provided
            dress.save()
        return dress

class DressRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    dress = serializers.PrimaryKeyRelatedField(queryset=models.Dress.objects.all())

    class Meta:
        model = models.DressRating
        fields = ['user', 'dress', 'rating', 'comment', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
        }

    def create(self, validated_data):
        # Prevent a user from rating the same dress more than once
        if models.DressRating.objects.filter(user=validated_data['user'], dress=validated_data['dress']).exists():
            raise serializers.ValidationError("You have already rated this dress.")
        
        return models.DressRating.objects.create(**validated_data)
