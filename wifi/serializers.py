from django.db import models
from rest_framework import serializers
from .models import NetworkModel, Devices, Avg


class NetworkModelSerializer(serializers.ModelSerializer):
    objects = models.Manager()

    class Meta:
        model = NetworkModel
        fields = ('id', 'auth')


class DevicesSerializer(serializers.ModelSerializer):
    objects = models.Manager()

    class Meta:
        model = Devices
        fields = ('device_id', 'network_id', 'throughput')


class AvgSerializer(serializers.ModelSerializer):
    objects = models.Manager()

    class Meta:
        model = Avg
        fields = ('network_id', 'avg_throughput', 'no_of_devices')

