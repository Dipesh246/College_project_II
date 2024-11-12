# Generated by Django 4.2 on 2024-11-10 11:04

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Responder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_available', models.BooleanField(default=True)),
                ('current_location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('license_number', models.CharField(blank=True, max_length=50, null=True)),
                ('vehicle_number', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ASSIGNED', 'Assigned'), ('COMPLETED', 'Completed')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_responder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='responder.responder')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
