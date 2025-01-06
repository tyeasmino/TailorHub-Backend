from rest_framework import viewsets
from .models import DressType, DressMeasurement
from .serializers import DressTypeSerializer, DressMeasurementSerializer
 
class DressTypeViewSet(viewsets.ModelViewSet):
    queryset = DressType.objects.all()
    serializer_class = DressTypeSerializer
 
class DressMeasurementViewSet(viewsets.ModelViewSet):
    queryset = DressMeasurement.objects.all()
    serializer_class = DressMeasurementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        dress_type_id = self.request.query_params.get('dress_type', None)
        fit_finder_id = self.request.query_params.get('fit_finder', None)
        
        if dress_type_id:
            queryset = queryset.filter(dress_type_id=dress_type_id)
        
        if fit_finder_id: 
            queryset = queryset.filter(fit_finder_id=fit_finder_id)
        
        return queryset

    def perform_create(self, serializer): 
        serializer.save()
