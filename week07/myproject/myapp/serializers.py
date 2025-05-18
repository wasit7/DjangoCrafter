# /myproject/myapp/serializers.py
from rest_framework import serializers
from .models import Bike

class BikeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Bike
        fields = ['id', 'name', 'is_available', 'hourly_rate', 'description', 'image']