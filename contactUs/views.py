from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ContactUsSerializer
from .models import ContactUs


# Create your views here.
class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer 