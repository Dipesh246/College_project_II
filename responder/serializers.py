from datetime import timedelta, datetime
from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Responder, EmergencyRequest
from user.models import User

class ResponderCreateSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = Responder
        fields = ['user', 'is_available', 'latitude', 'longitude']

    def create(self, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        if latitude and longitude:
            validated_data['current_location'] = Point(longitude, latitude)
        return super().create(validated_data)

class ResponderPatchSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = Responder
        fields = ['id', 'user', 'is_available', 'latitude', 'longitude']
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        if latitude and longitude:
            instance.current_location = Point(longitude, latitude)
        return super().update(instance, validated_data)

class ResponseGetSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = Responder
        fields = ['id','latitude', 'longitude']  # Include any other relevant fields

    def get_latitude(self, obj):
        # If location is a PointField
        if isinstance(obj.current_location, Point):
            return obj.current_location.y  # Latitude is stored in the 'y' attribute of PointField
        return None

    def get_longitude(self, obj):
        # If location is a PointField
        if isinstance(obj.current_location, Point):
            return obj.current_location.x  # Longitude is stored in the 'x' attribute of PointField
        return None

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responder
        fields = ['id', 'user', 'is_available', 'current_location']

class EmergencyRequestCreateSerializer(serializers.ModelSerializer):

    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = EmergencyRequest
        fields = [
            'latitude', 
            'longitude'
        ]

    def create(self, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        user = self.context['request'].user
        if latitude and longitude:
            validated_data['request_location'] = Point(longitude, latitude)

        validated_data['customer'] = user
        return super().create(validated_data)        

class EmergencyRequestSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    assigned_responder = ResponderSerializer(read_only=True)
    class Meta:
        model = EmergencyRequest
        fields = [
            'id', 'customer', 'request_location', 'status',
            'assigned_responder', 'created_at',
        ]

class EmergencyRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyRequest
        fields = [
            'id',
            'status',
        ]
