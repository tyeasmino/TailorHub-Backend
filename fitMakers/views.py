from django.shortcuts import render
from rest_framework import viewsets 
from . import models, serializers


# Create your views here.
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class FitMakerViewSet(viewsets.ModelViewSet):
    queryset = models.FitMaker.objects.all()
    serializer_class = serializers.FitMakerSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return SkillSeeker.objects.filter(user = self.request.user)
    