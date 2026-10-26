from ncclient import manager

def connect_netconf(hosts):
   username = "admin"
   password = "admin"
   if hosts == "172.100.100.4":
      password="NokiaSrl1!"
   return manager.connect(
   host=hosts,
   port=830,
   username="admin",
   password=password,
   hostkey_verify=False,
   timeout=15,
   )

import xml.dom.minidom

def xml_parsing(string_param):
    return xml.dom.minidom.parseString(string_param)
