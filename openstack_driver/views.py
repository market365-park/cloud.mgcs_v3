# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from datetime import datetime, timedelta


from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import TemplateView
from openstackclient.compute.v2 import server as trans_format
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from openstack_driver.drivers import ceilometer_driver
from openstack_driver.drivers import compute_driver
from openstack_driver.drivers import image_driver
from openstack_driver.drivers import network_driver
from openstack_driver.drivers import orchestration_driver

class HypervisorView(TemplateView):
    template_name = 'admin/hypervisors.html'

class InstanceView(TemplateView):
    template_name = 'compute/launch_instance.html'

class ComputeView(TemplateView):
    template_name = 'compute/instance_list.html'

class ImageView(TemplateView):
    template_name = 'compute/image.html'

class NetworkView(TemplateView):
    template_name = 'network/network.html'

class TopologyView(TemplateView):
    template_name = 'network/topology.html'

class RouterView(TemplateView):
    template_name = 'network/router.html'

class StorageView(TemplateView):
    template_name = 'compute/storage.html'

class MeteringView(TemplateView):
    template_name = 'metering/metering.html'


@api_view(['POST', 'GET'])
def server(request):
    if request.method == 'GET':
        data = {'servers':[]}
        servers = compute_driver.get_servers()
        for server in servers:
            zone_name = getattr(server, 'OS-EXT-AZ:availability_zone')
            image_name = image_driver.get_image_name(server.image['id'])
            flavor_name = compute_driver.get_flavor_detail(server.flavor['id']).name
            server_state = trans_format._format_servers_list_power_state(getattr(server, 'OS-EXT-STS:power_state'))
            # ip = compute_driver.get_ips(server.id)
            now = datetime.now()
            server_start = datetime.strptime(server.created, "%Y-%m-%dT%H:%M:%SZ")


            data['servers'].append(
                {
                    'name': server.name,
                    'image': image_name,
                    'flavor' : flavor_name,
                    'created': now-server_start,
                    # 'addresses': server.addresses,
                    'status': server.status,
                    'power': server_state,
                    'zone': zone_name,
                }
            )
        return JsonResponse(data)

    elif request.method == 'POST':
        orchestration_driver.create_stack(request.data)
        data = {}
        return Response(data, status=status.HTTP_201_CREATED)
    return HttpResponse("REST API for Servers1")

@api_view(['POST', 'GET'])
def server_detail(request):
    if request.method == 'GET':
        data = {'server_details':[]}
        servers = compute_driver.get_servers()
        for server in servers:
            image_name = image_driver.get_image_name(server.image['id'])
            flavor_cpu = compute_driver.get_flavor_detail(server.flavor['id']).vcpus
            flavor_ram = compute_driver.get_flavor_detail(server.flavor['id']).ram
            flavor_disk = compute_driver.get_flavor_detail(server.flavor['id']).disk
            server_state = trans_format._format_servers_list_power_state(getattr(server, 'OS-EXT-STS:power_state'))
            data['server_details'].append(
                {
                    'name': server.name,
                    'image': image_name,
                    'flavor_cpu' : flavor_cpu,
                    'flavor_ram': flavor_ram,
                    'flavor_disk': flavor_disk,
                    'created': server.created,
                    'status': server.status,
                    'power': server_state,
                }
            )
        return JsonResponse(data)

    return HttpResponse("REST API for server2")

@api_view(['GET'])
def image(request):
    if request.method == 'GET':
        data = {'images': []}
        images = image_driver.get_images()
        for image in images:
            data['images'].append({
                'id': image.id,
                'name': image.name,
                'status': image.status,
                #'image_type': image.image_type,
                'disk_format': image.disk_format,
                'created_at': image.created_at,
                'protected': image.protected,
                'size': image.size,
                'min_disk': image.min_disk,
            })
        return JsonResponse(data)
    return HttpResponse("REST API for Images")

@api_view(['GET'])
def flavor(request):
    if request.method == 'GET':
        data = {'flavors': []}
        flavors = compute_driver.get_flavors()
        for flavor in flavors:
            data['flavors'].append({
                'name': flavor.name,
                'vcpus': flavor.vcpus,
                'ram': flavor.ram,
                'disk': flavor.disk
            })
        return JsonResponse(data)
    return HttpResponse("REST API for flavors")

@api_view(['GET'])
def zone(request):
    if request.method == 'GET':
        data = {'zones': []}
        zones = compute_driver.get_zones(detailed=False)
        for zone in zones:
            if zone.zoneName == 'internal':
                continue
            else:
                data['zones'].append({
                    'name': zone.zoneName
                })
        return JsonResponse(data)
    return HttpResponse("REST API for flavors")

@api_view(['GET'])
def network(request):
    if request.method == 'GET':
        networks = network_driver.get_networks()
        return JsonResponse(networks)
    return HttpResponse("REST API for networks")

@api_view(['GET'])
def resource(request):
    if request.method == 'GET':
        resources = compute_driver.get_resources()
        data = {'resources': {}}
        for resource in resources:
            data['resources'][resource.name] = resource.value
            # print ("{} : {}".format(resource.name, resource.value))
        return JsonResponse(data)
    return HttpResponse("REST API for resources")

@api_view(['GET'])
def hypervisor(request):
    if request.method == 'GET':
        data = {'hypervisors':[]}
        hypervisors = compute_driver.get_hypervisors()
        for hypervisor in hypervisors:
            data['hypervisors'].append({
                'id':hypervisor.id,
                'host_name':hypervisor.hypervisor_hostname,
                'running_vms':hypervisor.running_vms,
                'total_cpu':hypervisor.vcpus,
                'used_cpu':hypervisor.vcpus_used,
                'free_cpu':hypervisor.vcpus-hypervisor.vcpus_used,
                'total_ram_mb':hypervisor.memory_mb,
                'used_ram_mb': hypervisor.memory_mb_used,
                'free_ram_mb': hypervisor.memory_mb-hypervisor.memory_mb_used,
                'total_disk_gb': hypervisor.local_gb,
                'used_disk_gb': hypervisor.local_gb_used,
                'free_disk_gb': hypervisor.local_gb-hypervisor.local_gb_used
            })
        return JsonResponse(data)

    return HttpResponse("REST API for Hypervisor")

@api_view(['GET', 'POST'])
def meter(request):
    if request.method == 'POST':
        data = {'meters': []}
        servers = compute_driver.get_servers()
        resources = ceilometer_driver.get_resources_list()

        index = 0
        for server in servers:
            instance_name = server.name
            flavor = compute_driver.get_flavor_detail(server.flavor['id'])
            meter_start = datetime.strptime(request.data['start'], "%Y-%m-%dT%H:%M:%S")
            meter_end = datetime.strptime(request.data['end'], "%Y-%m-%dT%H:%M:%S")
            server_start = datetime.strptime(server.created, "%Y-%m-%dT%H:%M:%SZ")
            # print ("Instance Name : " + instance_name)
            # print ("Flavor Name : " + flavor_name)
            if meter_start < server_start:
                duration = meter_end - server_start
                if duration <= timedelta(seconds=0):
                    duration = timedelta(0)
            else:
                duration = meter_end-meter_start

            data['meters'].append({
                'instance_name': instance_name,
                'flavor_name': flavor.name,
                'vcpus': flavor.vcpus,
                'ram': flavor.ram/1024,
                'duration_days': duration.days,
                'duration_hours': duration.seconds/3600,
                'network_interfaces': []
            })

            for resource in resources:
                pattern = re.compile(r"^instance-.{8}-" + server.id)
                match = pattern.search(resource.resource_id)
                if match:

                    # print ("vNic Name : " + resource.metadata['vnic_name'])
                    # query_init = [dict(field='resource_id', op='eq', value=resource.resource_id)]

                    query_search = [
                        dict(field='resource_id', op='eq', value=resource.resource_id),
                        dict(field='timestamp', op='ge', value=request.data['start']),
                        dict(field='timestamp', op='le', value=request.data['end'])
                    ]
                    # statistics_tmp = ceilometer_driver.get_statistics_list(meter_name='network.outgoing.bytes', q=query_init)
                    statistics = ceilometer_driver.get_statistics_list(meter_name='network.outgoing.bytes', q=query_search, period=86400)
                    length = len(statistics)

                    if not statistics:
                        # print ("사용량 없음")
                        # print ("---------------------------------------")
                        data['meters'][index]['network_interfaces'].append({
                            'name': resource.metadata['vnic_name'],
                            'tx': 0
                        })
                    else:
                        # if start < datetime.strptime(statistics_tmp[0].duration_start[:19],"%Y-%m-%dT%H:%M:%S").date() :
                        if meter_start < server_start:
                            # print ("Network Usage : {} GB".format(round((statistics[length - 1].max / 1073741824), 2)))
                            # print ("---------------------------------------")
                            data['meters'][index]['network_interfaces'].append({
                                'name': resource.metadata['vnic_name'],
                                'tx': round((statistics[length - 1].max / 1073741824), 2)
                            })
                        elif meter_start == meter_end :
                            data['meters'][index]['network_interfaces'].append({
                                'name': resource.metadata['vnic_name'],
                                'tx': round((statistics[0].max / 1073741824), 2)
                            })
                        else:
                            # print ("Network Usage : {} GB".format(
                            #     round((statistics[length - 1].max - statistics[0].max) / 1073741824), 2))
                            # print ("---------------------------------------")
                            data['meters'][index]['network_interfaces'].append({
                                'name': resource.metadata['vnic_name'],
                                'tx': round(((statistics[length - 1].max - statistics[0].max) / 1073741824), 2)
                            })
            index = index + 1
        return JsonResponse(data)
        # resources = ceilometer_driver.get_resources_list()
        #
        # for resource in resources:
        #     if len(resource.resource_id) > 60:
        #         print ("Instance Name : " + resource.metadata['display_name'])
        #         print ("Flavor Name : " + resource.metadata['flavor.name'])
        #         print ("vNic Name : " + resource.metadata['vnic_name'])
        #         query_init = [dict(field='resource_id', op='eq', value=resource.resource_id)]
        #
        #         query_search = [
        #             dict(field='resource_id', op='eq', value=resource.resource_id),
        #             dict(field='timestamp', op='ge', value=request.data['start']),
        #             dict(field='timestamp', op='le', value=request.data['end'])
        #         ]
        #         statistics_tmp = ceilometer_driver.get_statistics_list(meter_name='network.outgoing.bytes', q=query_init)
        #         statistics = ceilometer_driver.get_statistics_list(meter_name='network.outgoing.bytes', q=query_search, period=86400)
        #         length = len(statistics)
        #         start = datetime.strptime(request.data['start'], "%Y-%m-%dT%H:%M:%S").date()
        #
        #         if not statistics:
        #             print ("사용량 없음")
        #             print ("---------------------------------------")
        #         else:
        #             if start < datetime.strptime(statistics_tmp[0].duration_start[:19],"%Y-%m-%dT%H:%M:%S").date() :
        #                 print ("Network Usage : {} GB".format(round((statistics[length - 1].max / 1073741824), 2)))
        #                 print ("---------------------------------------")
        #             else:
        #                 print ("Network Usage : {} GB".format(
        #                     round((statistics[length - 1].max - statistics[0].max) / 1073741824), 2))
        #                 print ("---------------------------------------")





    elif request.method == 'GET':
        return
    return HttpResponse("REST API for Meter")


# query_start = [
#     dict(field='resource_id', op='eq', value=resource.resource_id),
#     dict(field='timestamp', op='le', value=request.data['start'])
# ]
# samples_start = ceilometer_driver.get_samples_list(meter_name='network.outgoing.bytes', q=query_start, limit=1)
#
# query_end = [
#     dict(field='resource_id', op='eq', value=resource.resource_id),
#     dict(field='timestamp', op='le', value=request.data['end'])
# ]
# samples_end = ceilometer_driver.get_samples_list(meter_name='network.outgoing.bytes', q=query_end, limit=1)

# if (samples_end[0].counter_volume-samples_start[0].counter_volume) < 0:
#     print ("사용량 없음")
#     print ("---------------------------------------")
# else :
#     print ("Network Usage : {} GB".format(round((samples_end[0].counter_volume-samples_start[0].counter_volume)/1073741824), 2))
#     print ("---------------------------------------")
