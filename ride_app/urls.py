from .users.user_view import UserViewSet
from .rides.rides_view import RideViewSet
from .ride_events.ride_events_view import RideEventViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from django.urls import path,include



router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'rideevents', RideEventViewSet, basename='rideevent')
urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]