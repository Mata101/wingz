from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from .filters import RideFilter
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    User = get_user_model()
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    filterset_class = RideFilter
    queryset=Ride.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        ordering_by_pickuptime = self.request.query_params.get('pickup_time', None)
        sort_by_pickup_time = {
            'asc': 'pickup_time',
            'desc': '-pickup_time'
        }
        
        sort_by_distance = {
            'asc': 'distance',
            'desc': '-distance'
        }
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        ordering_by_distance = self.request.query_params.get('distance')

        if lat and lng:
            user_location = Point(float(lng), float(lat), srid=4326)

        if ordering_by_pickuptime in ['asc', 'desc'] and (ordering_by_distance in ['asc', 'desc'] or (lat and lng)):
            if lat and lng:
                try:
                    
                    queryset = queryset.annotate(
                        distance=Distance('pickup_point', user_location)
                    )
                except (ValueError, TypeError):
                    pass
                
                queryset = queryset.order_by(sort_by_pickup_time[ordering_by_pickuptime],'distance' if ordering_by_distance not in ['asc', 'desc'] else sort_by_distance[ordering_by_distance])
        else:
            if ordering_by_pickuptime in ['asc', 'desc']:
                queryset = queryset.order_by(sort_by_pickup_time[ordering_by_pickuptime])


            if lat and lng:
                try:
                    
                    if ordering_by_distance in ['asc', 'desc']:
                        queryset = queryset.annotate(
                            distance=Distance('pickup_point', user_location)
                        ).order_by(sort_by_distance[ordering_by_distance])
                    else:
                        queryset = queryset.annotate(
                            distance=Distance('pickup_point', user_location)
                        ).order_by('distance')
                    
                except (ValueError, TypeError):
                    pass  # skip distance sort if input is invalid

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        ride = self.get_object()
        serializer = self.get_serializer(ride, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class RideEventViewSet(viewsets.ModelViewSet):
    serializer_class = RideEventSerializer
    
    queryset = Ride_Event.objects.all()

    def update(self, request, *args, **kwargs):
        ride_event = self.get_object()
        serializer = self.get_serializer(ride_event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)