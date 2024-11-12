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
    class Meta:
        model = Responder
        fields = '__all__'

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
            'customer', 
            'status',
            'assigned_responder', 
            'created_at', 
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