from rest_framework import serializers
from ..models import User
from django.contrib.auth import get_user_model


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
