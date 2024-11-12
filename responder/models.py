# from django.db import models
from django.contrib.gis.db import models
from user.models import User

class Responder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    current_location = models.PointField(geography=True, srid=4326)  # Geospatial field

    def __str__(self):
        return f"{self.user.username} - {self.user.vehicle_number}"
    

class EmergencyRequest(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    request_location = models.PointField(geography=True, srid=4326)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('ASSIGNED', 'Assigned'),
        ('COMPLETED', 'Completed'),
    ], default='PENDING')
    assigned_responder = models.ForeignKey(Responder, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.customer.username} - Status: {self.status}"