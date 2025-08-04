from rest_framework import viewsets
from rest_framework.response import Response
from ..models import User
from .user_serializer import *
from django.contrib.auth import get_user_model


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