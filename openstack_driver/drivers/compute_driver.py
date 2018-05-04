from novaclient import client as nvclient
from openstackclient.compute import client as osclient
from .auth import sess

novaClient = nvclient.Client("2.1", session=sess)

def get_flavors():
    return novaClient.flavors.list()

def get_flavor_detail(flavor_id):
    return novaClient.flavors.get(flavor_id)

def get_zones(**kwargs):
    return novaClient.availability_zones.list(**kwargs)

def get_zone_name(server_id):
    return novaClient.servers.zone(server_id)

def get_servers():
    return novaClient.servers.list()

def get_hypervisors():
    return novaClient.hypervisors.list()

def get_resources():
    return novaClient.limits.get().absolute

def get_volumes(**kwargs):
    return novaClient.get_server_volumes(**kwargs)
