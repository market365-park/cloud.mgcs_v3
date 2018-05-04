from neutronclient.v2_0 import client as ntclient
from .auth import sess

neutronClient = ntclient.Client(session=sess)

def get_networks(**kwargs):
	return neutronClient.list_networks(**kwargs)

def get_routers(**kwargs):
	return neutronClient.list_routers(**kwargs)
