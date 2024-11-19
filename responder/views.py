from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from rest_framework.permissions import IsAuthenticated
from .models import (
    Responder,
    EmergencyRequest,
)
from .serializers import (
    ResponderCreateSerializer,
    ResponderPatchSerializer,
    ResponseGetSerializer,
    EmergencyRequestSerializer,
    EmergencyRequestCreateSerializer,
    EmergencyRequestUpdateSerializer,
)
from django.db import transaction
from responder.service import get_shortest_path

class ResponderViewSet(viewsets.ModelViewSet):
    queryset = Responder.objects.all()
    serializer_class = ResponseGetSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = ResponseGetSerializer
        if self.request.method=='GET':
            serializer_class = ResponseGetSerializer
        elif self.request.method=='POST':
            serializer_class = ResponderCreateSerializer
        elif self.request.method=='PATCH':
            serializer_class = ResponderPatchSerializer
        
        
        return serializer_class
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

class EmergencyRequestViewSet(viewsets.ModelViewSet):
    queryset = EmergencyRequest.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Selects the serializer class based on the request method.
        """
        if self.request.method == 'GET':
            return EmergencyRequestSerializer
        elif self.request.method == 'POST':
            return EmergencyRequestCreateSerializer
        elif self.request.method == 'PATCH':
            return EmergencyRequestUpdateSerializer
        return EmergencyRequestSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @transaction.atomic
    @action(detail=True, methods=['patch'], url_path='assign')
    def assign_request(self, request, pk=None):
        try:
            emergency_request = EmergencyRequest.objects.get(pk=pk, status='PENDING')
            responder = Responder.objects.get(user=request.user)
            emergency_request.status = 'ASSIGNED'
            emergency_request.assigned_responder = responder
            emergency_request.save()
            return Response({"status": "Request assigned successfully."}, status=status.HTTP_200_OK)
        except EmergencyRequest.DoesNotExist:
            return Response({"error": "Emergency request not found or already assigned."}, status=status.HTTP_404_NOT_FOUND)
        except Responder.DoesNotExist:
            return Response({"error": "Responder not found."}, status=status.HTTP_404_NOT_FOUND)    
    
    @action(detail=False, methods=['get'], url_path="temporary-paths")
    def temporary_path(self, request):
        try:
            lat = float(request.GET.get("latitude"))
            lon = float(request.GET.get("longitude"))
            customer_location = (lat, lon)

            customer_pont = Point(lon, lat, srid=4326)
            responders = Responder.objects.all()
            paths=[]

            for responder in responders:
                responder_location = (responder.current_location.y, responder.current_location.x)
                path_coords = get_shortest_path(customer_location, responder_location)
                print(path_coords)
                if path_coords:
                    paths.append({
                        "responder_id": responder.user.id,
                        "username": responder.user.username,
                        "coordinates": path_coords
                    })
            
            return Response({"paths":paths}, status=status.HTTP_200_OK)
        

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





