from ncclient import manager
HOST = "172.100.100.4"

def connect_netconf():

    return manager.connect(
    host=HOST,
    port=830,
    username="admin",
    password="admin",
    hostkey_verify=False,
    timeout=15,
)

import xml.dom.minidom

def xml_parsing(string_param):
    return xml.dom.minidom.parseString(string_param)
