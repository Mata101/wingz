from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.utils import timezone
from datetime import timedelta


class UserSerializer(serializers.ModelSerializer):
    User = get_user_model()
    role = serializers.ChoiceField(
        choices=User._meta.get_field('role').choices,
        default='rider',
        help_text="Ride Status"
    )
    class Meta:
        model = get_user_model()
        fields = [
            'id_user',
            'role',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password'
        ]
        read_only_fields = ['id_user']

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

class RideSerializer(serializers.ModelSerializer):
    User = get_user_model()

    id_rider = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_driver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.ChoiceField(
        choices=Ride._meta.get_field('status').choices,
        default='en-route',
        help_text="Ride Status"
    )

    todays_ride_events = serializers.SerializerMethodField()

    pickup_latitude = serializers.FloatField(write_only=True)
    pickup_longtitude = serializers.FloatField(write_only=True)
    dropoff_latitude = serializers.FloatField(write_only=True)
    dropoff_longtitude = serializers.FloatField(write_only=True)
    

    class Meta:
        model = Ride
        fields = [
            'id_ride',
            'status',
            'id_rider',
            'id_driver',
            'pickup_latitude',
            'pickup_longtitude',
            'dropoff_latitude',
            'dropoff_longtitude',
            'pickup_time',
            'todays_ride_events',
            'pickup_point',
            'dropoff_point',
        ]
        read_only_fields = ['id_ride', 'pickup_point', 'dropoff_point']

    def get_todays_ride_events(self, ride):
        last_24_hours = timezone.now() - timedelta(hours=24)
        # print(last_24_hours)
        events = ride.todays_ride_events.filter(created_at__gte=last_24_hours)
        return RideEventSerializer(events, many=True).data
    
    def create(self, validated_data):
        pickup_lat = validated_data.pop('pickup_latitude')
        pickup_lng = validated_data.pop('pickup_longtitude')
        dropoff_lat = validated_data.pop('dropoff_latitude')
        dropoff_lng = validated_data.pop('dropoff_longtitude')

        validated_data['pickup_point'] = Point(pickup_lng, pickup_lat)
        validated_data['dropoff_point'] = Point(dropoff_lng, dropoff_lat)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'pickup_latitude' in validated_data and 'pickup_longtitude' in validated_data:
            lat = validated_data.pop('pickup_latitude')
            lng = validated_data.pop('pickup_longtitude')
            instance.pickup_point = Point(lng, lat)

        if 'dropoff_latitude' in validated_data and 'dropoff_longtitude' in validated_data:
            lat = validated_data.pop('dropoff_latitude')
            lng = validated_data.pop('dropoff_longtitude')
            instance.dropoff_point = Point(lng, lat)

        return super().update(instance, validated_data)



