from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ResponderViewSet,
    EmergencyRequestViewSet
)

router = DefaultRouter(trailing_slash=False)
router.register(r'responders', ResponderViewSet, basename='responder')
router.register(r'emergency-request',EmergencyRequestViewSet, basename='requester')

urlpatterns = [
    path('', include(router.urls)),
]
