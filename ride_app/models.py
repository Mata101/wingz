from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.utils import timezone

# Create your models here.

ROLES = [
        ('admin', 'Admin'),
        ('rider', 'Rider'),
        ('driver', 'Driver')
    ]
STATUS = [
            ('en-route', 'En-Route'),
            ('pickup', 'Pickup'),
            ('dropoff', 'Dropoff'),
    ]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.role = 'admin'
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(email=email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True,db_comment="User ID")
    role = models.CharField(max_length=15,choices=ROLES,db_comment="User role")
    first_name = models.CharField(max_length=40,db_comment="User's first name")
    last_name = models.CharField(max_length=40,db_comment="User's last name")
    email = models.CharField(max_length=64,unique=True, db_comment="User's email address")
    phone_number = models.CharField(max_length=20,db_comment="User's phone number")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'role']
    objects = CustomUserManager()


class Ride(models.Model):
    id_ride = models.AutoField(primary_key=True,db_comment="Ride ID")
    status = models.CharField(max_length=10,choices=STATUS,db_comment="Ride Status")
    id_rider = models.ForeignKey(User,on_delete=models.CASCADE,db_comment="Foreign key referencing User(id_user)")
    id_driver = models.ForeignKey(User,on_delete=models.CASCADE,db_comment="Foreign key referencing User(id_user)",related_name='rides')
    pickup_point = gis_models.PointField(srid=4326, default=Point(0.0, 0.0),db_comment="Pickup location (longitude, latitude)")
    dropoff_point = gis_models.PointField(srid=4326, default=Point(0.0, 0.0),db_comment="Dropoff location (longitude, latitude)")
    pickup_time = models.DateTimeField(db_comment="Pickup time")


class Ride_Event(models.Model):
    id_ride_event = models.AutoField(primary_key=True,db_comment="Ride Event ID")
    id_ride = models.ForeignKey(Ride,on_delete=models.CASCADE,related_name='todays_ride_events',db_comment="Foreign key referencing Ride(id_ride)")
    description = models.CharField(max_length=100,db_comment="Description of the ride event",blank=True)
    created_at = models.DateTimeField(default=timezone.now,db_comment="Timestamp of when the event occurred")