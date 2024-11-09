from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSet

router = DefaultRouter(trailing_slash=False)

router.register('user', UserViewSet, basename="user")

urlpatterns = [
    
]+ router.urls
