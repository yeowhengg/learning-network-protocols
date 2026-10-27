from netconf_reusable import connect_netconf, xml_parsing

class Helpers:
   def __init__(self):
      pass

   def format_xml(self, xml_data):
      return xml_parsing(xml_data).toprettyxml()
      
class Filters:
   def __init__(self):
      pass

   def get_interface_filter(self):
      return """
         <interfaces xmlns="http://openconfig.net/yang/interfaces">
            <interface>
               <name>Ethernet1</name>
               <state>
                     <name/>
                     <admin-status/>
                     <oper-status/>
                     <mtu/>
               </state>
            </interface>
         </interfaces>
      """

class VendorAutomation:
   def __init__(self, participants: list):
      self.participants = participants
      self.filters = Filters()
      self.helpers = Helpers()

   def get_interfaces(self):
      for participant_ip in self.participants:
         with connect_netconf(participant_ip) as conn:
            resp = conn.get(filter=("subtree", self.filters.get_interface_filter())).data_xml
            formatted = self.helpers.format_xml(resp)
            print(formatted)

hosts = ["172.100.100.2", "172.100.100.2"]

automation = VendorAutomation(hosts)
automation.get_interfaces()
