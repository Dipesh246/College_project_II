from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from user.models import User
from user.serializers import UserSerializer
from user.validators import validate_password_strength
from django.core.exceptions import ValidationError

class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })
            except ValidationError as e:
                return Response({'error': e.messages}, 
                              status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, 
                      status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
            
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')
        
        if not request.user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        if new_password != confirm_new_password:
            return Response({'error': 'New passwords don\'t match'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        try:
            validate_password_strength(new_password)
            request.user.set_password(new_password)
            request.user.save()
            return Response({'message': 'Password changed successfully'})
        except ValidationError as e:
            return Response({'error': e.messages}, 
                          status=status.HTTP_400_BAD_REQUEST)
