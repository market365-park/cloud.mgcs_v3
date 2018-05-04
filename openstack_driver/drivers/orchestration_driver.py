import yaml
from heatclient import client as hclient
from heatclient.common import template_utils

from .auth import sess

def create_stack(instance_info):
    # data = {'resources':{'my_instance':{'type':'OS::Nova::Server', 'properties':{'name':str(instance_info['name']),'image':str(instance_info['image']),'flavor':str(instance_info['flavor']),'networks':[{'network':'VM-Network01'}]}}}}
    data = {"resources": {
        "my_instance": {"type": "OS::Nova::Server",
                        "properties": {"name": str(instance_info['name']), "image": str(instance_info['image']),
                                       "flavor": str(instance_info['flavor']),
                                       "networks": [{"port": "{get_resource: instance_port}"}]}},
        "instance_port": {"type": "OS::Neutron::Port",
                          "properties": {"network": "VM-Network01", "security_groups": ["default"]}},
        "floating_ip": {"type": "OS::Neutron::FloatingIP", "properties": {"floating_network": "Ex-Network01"}},
        "association": {"type": "OS::Neutron::FloatingIPAssociation",
                        "properties": {"floatingip_id": "{get_resource: floating_ip}",
                                       "port_id": "{get_resource: instance_port}"}}
    },
        "outputs": {"instance_name": {"description": "Name of the instance", "value": "{get_attr:[my_instance, name]}"},
                    "instance_id": {"description": "UUID of the instance", "value": "{get_resource: my_instance}"},
                    # "instance_image_name":{"description":"Name of the image","value":"{get_attr:[my_instance, image]}"},
                    # "instance_flavor_name":{"description":"Name of the flavor","value":"{get_attr:[my_instance, flavor]}"},
                    "instance_public_ip": {"description": "Floating IP address",
                                           "value": "{get_attr:[floating_ip, floating_ip_address]}"}

                    }
    }

    stack = yaml.dump(data, default_flow_style=False)
    stack = stack.replace("'", "")

    file_path = "/etc/openstack/heat/%s-stack.yml" % (instance_info['name'])
    with open(file_path, 'w') as f:
        # f.write('heat_template_version: 2013-05-23\n')
        f.write('heat_template_version: 2016-04-08\n')
        f.write('description: Simple template to deploy a single compute instance\n')
        f.write(stack)

    heat = hclient.Client("1", session=sess)

    template_file = file_path
    template_url = ''
    template_object = ''

    tpl_files, template = template_utils.get_template_contents(template_file, template_url, template_object)

    stack_name = "%s-%s-stack" % (str(instance_info['owner']), str(instance_info['name']))

    fields = {
        'stack_name': stack_name,
        'template': template
    }

    heat.stacks.create(**fields)

    return


def delete_stack(stack_name):
    heat = hclient.Client("1", session=sess)
    fields = {'stack_id': stack_name}

    heat.stacks.delete(**fields)
    return


def get_stack():
    heat = hclient.Client("1", session=sess)
    return heat.stacks.list()


def get_stack_detail(stack_name):
    heat = hclient.Client("1", session=sess)
    stack = heat.stacks.get(stack_name)

    return stack.outputs
