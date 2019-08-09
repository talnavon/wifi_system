from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import NetworkModel, Devices, Avg
from .serializers import NetworkModelSerializer, DevicesSerializer, AvgSerializer


# This function return Json object of Wifi Network
@api_view(['GET'])
def fetch_network_by_id(request, id):
    if request.method == 'GET':
        networks = NetworkModel.objects.filter(id=id)
        devices = Devices.objects.filter(network_id=id)
        serializer_network = NetworkModelSerializer(networks, many=True)
        serializer_devices = DevicesSerializer(devices, many=True)
        # if a network with this id exists:
        if len(serializer_network.data) > 0:
            serializer_dict = serializer_network.data[0]
            get_avg_throughput_from_avg_table(id, serializer_dict)
            devices_list = []
            for device in serializer_devices.data:
                device_dict = {"id": device["device_id"]}
                devices_list.append(device_dict)
            serializer_dict["devices"] = devices_list
            return Response(serializer_dict)
        else:
            return Response(status=status.HTTP_200_OK)


# This function gets id from the url and the serializer_dict and return the avg_throughput from the avg table
def get_avg_throughput_from_avg_table(network_id, serializer_dict):
    avg_network = Avg.objects.filter(network_id=network_id)
    serializers_avg = AvgSerializer(avg_network, many=True)
    if len(serializers_avg.data) > 0:
        serializer_dict["avg_throughput"] = serializers_avg.data[0]["avg_throughput"]
    else:
        serializer_dict["avg_throughput"] = 0


# This function return response of HTTP_201_CREATED if a device or/and network were added, else HTTP_400_BAD_REQUEST
@api_view(['POST'])
def connect_device_to_network(request):
    if request.method == 'POST':
        data_for_network = {'id': request.data.get('network_id'), 'auth': request.data.get('auth')}
        data_for_device = {'device_id': request.data.get('device_id'), 'network_id': request.data.get('network_id')}

        serializer_for_network = NetworkModelSerializer(data=data_for_network)
        serializer_for_devices = DevicesSerializer(data=data_for_device)
        network = NetworkModel.objects.filter(id=request.data.get('network_id'))
        serializers_for_avg = change_avg_table_values_for_specific_network(request,network)
        # if such network exists
        if len(network) > 0:
            if serializer_for_devices.is_valid() and serializers_for_avg.is_valid():
                serializer_for_devices.save()
                serializers_for_avg.save()
                return Response("A new device was added", status=status.HTTP_201_CREATED)
            else:
                return Response("Device data is wrong or device already exist", status=status.HTTP_400_BAD_REQUEST)
        else:
            # need to create a new network
            if serializer_for_network.is_valid() and serializers_for_avg.is_valid():
                serializer_for_network.save()
                serializers_for_avg.save()
                return Response("A new network and new device was added", status=status.HTTP_201_CREATED)
        return Response("Network data is wrong or network already exist", status=status.HTTP_400_BAD_REQUEST)


# This function gets the request and list of NetworkModel and return the changed avg table values for specific_network
def change_avg_table_values_for_specific_network(request, network):
    avg_network = Avg.objects.filter(network_id=request.data.get('network_id'))
    serializers_avg_old_data = AvgSerializer(avg_network, many=True)
    if len(serializers_avg_old_data.data) > 0:
        avg_throughput = serializers_avg_old_data.data[0]["avg_throughput"]
        no_of_devices = serializers_avg_old_data.data[0]["no_of_devices"]
    else:
        avg_throughput = 0
        no_of_devices = 0

    data_for_avg_after_calc = {
        'network_id': request.data.get('network_id'),
        'avg_throughput': ((avg_throughput * no_of_devices) / (no_of_devices + 1)),
        'no_of_devices': no_of_devices + 1
    }
    return AvgSerializer(avg_network[0], data=data_for_avg_after_calc) if len(network) > 0 else AvgSerializer(data=data_for_avg_after_calc)


# This function return response of HTTP_200_OK if a device was updated, else HTTP_400_BAD_REQUEST
@api_view(['PUT'])
def report_network_throughput(request):
    if request.method == 'PUT':
        device = Devices.objects.filter(device_id=request.data.get('device_id'),
                                        network_id=request.data.get('network_id'))
        if len(device) > 0:
            serializer_for_old_thru = DevicesSerializer(device[0], data=request.data)
            if serializer_for_old_thru.is_valid():
                old_throughput = serializer_for_old_thru.data["throughput"]
                recalculate_throughput_in_avg_table(request, old_throughput)
                serializer_for_devices = DevicesSerializer(device[0], data=request.data)
                serializer_for_devices.is_valid()
                serializer_for_devices.save()
                serializer_dict = serializer_for_devices.data
                return Response(serializer_dict, status=status.HTTP_200_OK)
            else:
                return Response(serializer_for_old_thru.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# This function gets the request and serializer_for_devices and changes the values in the avg table
def recalculate_throughput_in_avg_table(request, old_throughput):
    new_throughput = float(request.data.get('throughput'))
    avg_network = Avg.objects.filter(network_id=request.data.get('network_id'))
    serializer_for_avg = AvgSerializer(avg_network[0], data=request.data)

    if serializer_for_avg.is_valid():
        no_of_devices = serializer_for_avg.data["no_of_devices"]
        old_avg_throughput = float(serializer_for_avg.data["avg_throughput"])
        data_for_avg_after_calc = {
            'network_id': request.data.get('network_id'),
            'avg_throughput': (((old_avg_throughput * no_of_devices) -
                                float(old_throughput) + float(new_throughput)) / no_of_devices),
            'no_of_devices': no_of_devices
        }
        serializers_for_avg = AvgSerializer(avg_network[0], data=data_for_avg_after_calc)
        if serializers_for_avg.is_valid():
            serializers_for_avg.save()
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
