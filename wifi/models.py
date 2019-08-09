from django.db import models


class NetworkModel(models.Model):
    """
    Network Model
    Defines the attributes of a Wifi Network
    """
    id = models.CharField(primary_key=True, max_length=500)
    auth = models.CharField(max_length=6)
    objects = models.Manager()

    def get_id(self):
        return self.id


class Devices(models.Model):
    """
    Devices Model
    Defines the attributes of Devices
    """
    device_id = models.CharField(primary_key=True, max_length=500)
    network_id = models.IntegerField()
    throughput = models.FloatField(default=0)
    objects = models.Manager()

    def get_device_id(self):
        return self.device_id


class Avg(models.Model):
    """
    Avg Model
    Defines the attributes of Avg
    """
    network_id = models.CharField(primary_key=True, max_length=500)
    avg_throughput = models.FloatField(default=0)
    no_of_devices = models.IntegerField(default=0)
    objects = models.Manager()

    def get_network_id(self):
        return self.network_id
