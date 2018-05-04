"""mgcs_v3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include, path
from openstack_driver import views
from openstack_driver.views import InstanceView, ComputeView, ImageView, NetworkView, MeteringView, StorageView, \
    TopologyView, RouterView, HypervisorView

app_name = 'openstack'
urlpatterns = [
    path('hypervisor/', HypervisorView.as_view(), name='admin_hypervisor'),

    path('make_instance/', InstanceView.as_view(), name='make_instance'),
    path('instances/', ComputeView.as_view(), name='instances'),
    path('image/', ImageView.as_view(), name='image'),
    path('storage/', StorageView.as_view(), name='storage'),

    path('network/', NetworkView.as_view(), name='network'),
    path('topology/', TopologyView.as_view(), name='topology'),
    path('router/', RouterView.as_view(), name='router'),

    path('metering/', MeteringView.as_view(), name='metering'),


    path('rest/v2/images/', views.image, name='rest_images'),
    path('rest/v2/networks/', views.network, name='rest_networks'),
    path('rest/servers/', views.server, name='rest_servers'),
    path('rest/server_detail/', views.server_detail, name='rest_server_detail'),
    path('rest/flavors/detail/', views.flavor, name='rest_flavors'),
    path('rest/zones/', views.zone, name='rest_zones'),
    path('rest/v1/hypervisors/', views.hypervisor, name='restapi_hypervisor'),
    path('rest/v2/meters/', views.meter, name='rest_meters'),
    path('rest/resources/', views.resource, name='rest_resource'),
]