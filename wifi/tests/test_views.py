import json
from rest_framework import status
from django.test import Client
from django.urls import reverse
from django.test import TestCase
from ..models import NetworkModel, Devices, Avg

# initialize the APIClient app
client = Client()


class ViewsTest(TestCase):
    def setUp(self):
        self.device = Devices.objects.create(
            device_id='894', network_id='222', throughput='0')
        self.network = NetworkModel.objects.create(
            id='222', auth='0')
        self.avg = Avg.objects.create(
            network_id='222', avg_throughput='0', no_of_devices='1')
        self.connect1 = {
            'device_id': '123',
            'network_id': '222',
            'auth': 'public'
        }
        self.connect2 = {
            'device_id': '8585',
            'network_id': '',
            'auth': 'public'
        }
        self.report1 = {
            'device_id': '894',
            'network_id': '222',
            'throughput': '3636'
        }
        self.report2 = {
            'device_id': '111',
            'network_id': '222',
            'throughput': '54'
        }

    def test_connect_device_to_network(self):
        response = client.post(
            reverse('connect_device_to_network'),
            data=json.dumps(self.connect1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_connect_device_to_network_invalid_json(self):
        response = client.post(
            reverse('connect_device_to_network'),
            data=json.dumps(self.connect2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_report_network_throughput(self):
        response = client.put(
            reverse('report_network_throughput'),
            data=json.dumps(self.report1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_report_network_throughput_no_such_device_to_update(self):
        response = client.put(
            reverse('report_network_throughput'),
            data=json.dumps(self.report2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
