from django.shortcuts import render
from rest_framework import viewsets, generics
from . import models, serializers 


# Create your views here.
class FitFinderViewSet(viewsets.ModelViewSet):
    queryset = models.FitFinder.objects.all()
    serializer_class = serializers.FitFinderSerializer 
