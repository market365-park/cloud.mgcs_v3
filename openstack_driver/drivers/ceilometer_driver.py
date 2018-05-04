from .auth import sess
from ceilometerclient import client as ceiloclient

#ceilometerClient = ceiloclient.get_client("2",
#        os_username='testuser',
#        os_password='testuser',
#        os_tenant_name='test_project',
#        os_auth_url='http://10.12.14.31:5000/v3'
#    )

ceilometerClient = ceiloclient.get_client("2",
        os_username='admin',
        os_password='docker!23',
        os_tenant_name='devops',
        os_auth_url='http://10.12.14.36:5000/v3'
        )

def get_meters_list(**kwargs):
    return ceilometerClient.meters.list(**kwargs)

def get_samples_list(**kwargs):
    return ceilometerClient.samples.list(**kwargs)

def get_statistics_list(**kwargs):
    return ceilometerClient.statistics.list(**kwargs)

def get_resources_list(**kwargs):
    return ceilometerClient.resources.list(**kwargs)