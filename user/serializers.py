from rest_framework import serializers
from user.models import User
from django.contrib.auth.password_validation import validate_password
from .validators import validate_password_strength
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name', 
            'last_name', 
            'email', 
            'password', 
            'confirm_password',
            'user_type', 
            'phone_number', 
            'address', 
            'is_available', 
            'license_number', 
            'vehicle_number',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
        # Validate password strength
        try:
            validate_password_strength(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        # Check if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "Passwords don't match"})

        # Remove confirm_password from the data as we don't need to save it
        data.pop('confirm_password', None)
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


