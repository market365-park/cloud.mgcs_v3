from glanceclient import client as glclient
from novaclient import client as nvclient
from .auth import sess

glanceClient = glclient.Client("2", session=sess)

def get_images():
    return glanceClient.images.list()

def get_image_name(image_id):
    return glanceClient.images.get(image_id).name