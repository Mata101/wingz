from rest_framework import serializers
from ..models import Ride_Event,Ride


class RideEventSerializer(serializers.ModelSerializer):

    id_ride = serializers.PrimaryKeyRelatedField(
        queryset=Ride.objects.all(),
        help_text="Ride ID of the ride"
    )

    class Meta:
        model = Ride_Event
        fields = [
            'id_ride_event',
            'id_ride',
            'description',
            'created_at'
        ]

        read_only_fields = ['id_ride_event']