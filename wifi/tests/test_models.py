from django.test import TestCase

from ..models import NetworkModel, Devices, Avg


class WifiNetworkTest(TestCase):
    """ Test module for WifiNetwork model """

    def setUp(self):
        NetworkModel.objects.create(
            id='123456', auth='wpa')
        NetworkModel.objects.create(
            id='123', auth='public')
        Devices.objects.create(
            device_id='a1b2', network_id='123456', throughput=500)
        Devices.objects.create(
            device_id='a1b3', network_id='123', throughput=600)
        Avg.objects.create(
            network_id='123456', avg_throughput='500', no_of_devices=1)
        Avg.objects.create(
            network_id='123', avg_throughput='200', no_of_devices=1)

    def test_network(self):
        network1 = NetworkModel.objects.get(id='123456')
        network2 = NetworkModel.objects.get(id='123')
        self.assertEqual(
            network1.get_id(), '123456')
        self.assertEqual(
            network2.get_id(), '123')

    def test_devices(self):
        device1 = Devices.objects.get(device_id='a1b2')
        device2 = Devices.objects.get(device_id='a1b3')
        self.assertEqual(
            device1.get_device_id(), 'a1b2')
        self.assertEqual(
            device2.get_device_id(), 'a1b3')

    def test_avg(self):
        avg1 = Avg.objects.get(network_id='123456')
        avg2 = Avg.objects.get(network_id='123')
        self.assertEqual(
            avg1.get_network_id(), '123456')
        self.assertEqual(
            avg2.get_network_id(), '123')
