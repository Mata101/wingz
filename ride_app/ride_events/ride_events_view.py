from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Ride_Event
from .ride_events_serializer import *



class RideEventViewSet(viewsets.ModelViewSet):
    serializer_class = RideEventSerializer
    
    queryset = Ride_Event.objects.all()

    def update(self, request, *args, **kwargs):
        ride_event = self.get_object()
        serializer = self.get_serializer(ride_event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)