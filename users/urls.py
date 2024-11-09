from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

router = DefaultRouter(trailing_slash=False)

router.register('users', UserViewSet, basename="users")

urlpatterns = [
    
]+ router.urls
