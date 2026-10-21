# a simple connect with python

from ncclient import manager
from netconf_reusable import connect_netconf, xml_parsing


HOST = "172.100.100.4"
resp = None

with connect_netconf() as conn:
    print("NETCONF connected", conn.connected)
    print("Session ID: ", conn.session_id)
    module = None
    for capability in conn.server_capabilities:
        if "openconfig-interfaces" in str(capability):
            module = capability
            print("Openconfig interfaces: ", capability) # the supported openconfig interfaces in arista
            # RETURNS: Openconfig interfaces:  http://openconfig.net/yang/interfaces?module=openconfig-interfaces&revision=2026-01-06
            # module namespace = http://openconfig.net/yang/interfaces
            # supported yang module = openconfig-interfaces
            # revision = 2026-01-06

    # part 2
    # retrieving the actual YANG schema

    # params
    # identifier = supported yang module
    # version = revision
    # format = yang, json, xml, etc
    schema = conn.get_schema(
        identifier = "openconfig-interfaces",
        version= "2026-01-06",
        format="yang"
    )

    with open("openconfig-interfaces.yang", "w") as file:
        file.write(schema.data)

    print("schema saved")

    # out of code, use pyang to view the tree
    # pyang -p ./yang -f tree ./yang/openconfig-interfaces.yang


# we will face errors if there are no dependencies installed
# run openconfig-dependencies.py for openconfig-interfaces dependencies to install all dependencies

'''
Notes:

rw = configuration node
ro = read only node
* = repeated list entries
? = optional node
[name] list identified by a name key

looking at +-- rw interfaces, it is the module that can execute the following:
1. rw interface (write interface, editable)
1.2 within rw interface, we have the ro state (read only state) it provides the following:
    1. name?
    2. type
    3. mtu?
'''


"""
module: openconfig-interfaces
  +--rw interfaces
     +--rw interface* [name]
        +--rw name                  -> ../config/name
        +--rw config
        |  +--rw name?            string
        |  +--rw type             identityref
        |  +--rw mtu?             uint16
        |  +--rw loopback-mode?   oc-opt-types:loopback-mode-type
        |  +--rw description?     string
        |  +--rw enabled?         boolean
        +--ro state
        |  +--ro name?            string
        |  +--ro type             identityref
        |  +--ro mtu?             uint16
        |  +--ro loopback-mode?   oc-opt-types:loopback-mode-type
        |  +--ro description?     string
        |  +--ro enabled?         boolean
        |  +--ro ifindex?         uint32
        |  +--ro admin-status     enumeration
        |  +--ro oper-status      enumeration
        |  +--ro last-change?     oc-types:timeticks64
        |  +--ro logical?         boolean
        |  +--ro management?      boolean
        |  +--ro cpu?             boolean
        |  +--ro counters
        |     +--ro in-octets?               oc-yang:counter64
        |     +--ro in-pkts?                 oc-yang:counter64
        |     +--ro in-unicast-pkts?         oc-yang:counter64
        |     +--ro in-broadcast-pkts?       oc-yang:counter64
        |     +--ro in-multicast-pkts?       oc-yang:counter64
        |     +--ro in-errors?               oc-yang:counter64
        |     +--ro in-discards?             oc-yang:counter64
        |     +--ro out-octets?              oc-yang:counter64
        |     +--ro out-pkts?                oc-yang:counter64
        |     +--ro out-unicast-pkts?        oc-yang:counter64
        |     +--ro out-broadcast-pkts?      oc-yang:counter64
        |     +--ro out-multicast-pkts?      oc-yang:counter64
        |     +--ro out-discards?            oc-yang:counter64
        |     +--ro out-errors?              oc-yang:counter64
        |     +--ro last-clear?              oc-types:timeticks64
        |     +--ro in-unknown-protos?       oc-yang:counter64
        |     +--ro in-fcs-errors?           oc-yang:counter64
        |     x--ro carrier-transitions?     oc-yang:counter64
        |     +--ro interface-transitions?   oc-yang:counter64
        |     +--ro link-transitions?        oc-yang:counter64
        |     +--ro resets?                  oc-yang:counter64
        +--rw hold-time
        |  +--rw config
        |  |  +--rw up?     uint32
        |  |  +--rw down?   uint32
        |  +--ro state
        |     +--ro up?     uint32
        |     +--ro down?   uint32
        +--rw penalty-based-aied
        |  +--rw config
        |  |  +--rw max-suppress-time?    uint32
        |  |  +--rw decay-half-life?      uint32
        |  |  +--rw suppress-threshold?   uint32
        |  |  +--rw reuse-threshold?      uint32
        |  |  +--rw flap-penalty?         uint32
        |  +--ro state
        |     +--ro max-suppress-time?    uint32
        |     +--ro decay-half-life?      uint32
        |     +--ro suppress-threshold?   uint32
        |     +--ro reuse-threshold?      uint32
        |     +--ro flap-penalty?         uint32
        +--rw subinterfaces
           +--rw subinterface* [index]
              +--rw index     -> ../config/index
              +--rw config
              |  +--rw index?         uint32
              |  +--rw description?   string
              |  +--rw enabled?       boolean
              +--ro state
                 +--ro index?          uint32
                 +--ro description?    string
                 +--ro enabled?        boolean
                 +--ro name?           string
                 +--ro ifindex?        uint32
                 +--ro admin-status    enumeration
                 +--ro oper-status     enumeration
                 +--ro last-change?    oc-types:timeticks64
                 +--ro logical?        boolean
                 +--ro management?     boolean
                 +--ro cpu?            boolean
                 +--ro counters
                    +--ro in-octets?             oc-yang:counter64
                    +--ro in-pkts?               oc-yang:counter64
                    +--ro in-unicast-pkts?       oc-yang:counter64
                    +--ro in-broadcast-pkts?     oc-yang:counter64
                    +--ro in-multicast-pkts?     oc-yang:counter64
                    +--ro in-errors?             oc-yang:counter64
                    +--ro in-discards?           oc-yang:counter64
                    +--ro out-octets?            oc-yang:counter64
                    +--ro out-pkts?              oc-yang:counter64
                    +--ro out-unicast-pkts?      oc-yang:counter64
                    +--ro out-broadcast-pkts?    oc-yang:counter64
                    +--ro out-multicast-pkts?    oc-yang:counter64
                    +--ro out-discards?          oc-yang:counter64
                    +--ro out-errors?            oc-yang:counter64
                    +--ro last-clear?            oc-types:timeticks64
                    x--ro in-unknown-protos?     oc-yang:counter64
                    x--ro in-fcs-errors?         oc-yang:counter64
                    x--ro carrier-transitions?   oc-yang:counter64
        
"""

'''
In order to retrieve data with the schema, we need to think of it like a database query
SELECT oper_status
FROM interfaces
WHERE name = 'Ethernet1'

which roughly translates to:
/interfaces/interface[name=Ethernet1]/state/oper-status

the above line of string is our query filter.

structure:
  +--rw interfaces
    +--rw interface* [name]
        +--ro state
            |  +--ro name?            string
/interfaces (the module)/interface[name=...]/state/name

Instead of an sql query, we have to write the FILTER ourselves which is XML filter based.
'''

FILTER = """
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>Ethernet1</name>
        <state>
            <oper-status/>
        </state>
    </interface>
</interfaces>
"""

# we are requesting for <oper-status> values since it has no vlaue between the opening and closing tags

import xml.dom.minidom

with connect_netconf() as conn:
    resp = conn.get(filter=("subtree", FILTER)) # causes NCclient to construct a NETCONF <get> RPC. (remote procedure call)
'''
under the hood:

<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"
     message-id="101">

    <get>
        <filter type="subtree">
            <interfaces xmlns="http://openconfig.net/yang/interfaces">
                <interface>
                    <name>Ethernet1</name>
                    <state>
                        <oper-status/>
                    </state>
                </interface>
            </interfaces>
        </filter>
    </get>

</rpc>

is requested from the router via ncclient
'''

dom = xml_parsing(resp.data_xml)
print(dom.toprettyxml())
'''
<?xml version="1.0" ?>

(Represents the data portion of the RPC reply. Its namespace belongs to NETCONF, not OpenConfig)
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">

(This interface then is the openconfig namespace)
        <interfaces xmlns="http://openconfig.net/yang/interfaces">
                <interface>
                        <name>Ethernet1</name>
                        <state>
                                <oper-status>UP</oper-status>
                        </state>
                </interface>
        </interfaces>
</data>


'''

# another way of pretty printing
# resp.data_ele formats the DATA portion as xml element instead of the whole data_xml element

from lxml import etree

print(
    etree.tostring(
        resp.data_ele,
        pretty_print=True,
        encoding="unicode"
    )
)

'''
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name>Ethernet1</name>
      <state>
        <oper-status>UP</oper-status>
      </state>
    </interface>
  </interfaces>
</data>
'''


# getting only the operational status

root = resp.data_ele

NS = { # a NS for selecting XML element. "oc" would be the abbreviation similarly to e.g. import pandas as pd
    "oc": "http://openconfig.net/yang/interfaces"
}


# 
values = root.xpath(
    ".//oc:interface[oc:name='Ethernet1']/oc:state/oc:oper-status/text()",
    namespaces=NS
)

if values:
    print("Ethernet1 op status: ",values[0])
else:
    print("failed")

# difference between conn.get() and conn.get_config()

'''
get_config() retrives the configuration from a datastore

e.g.
CONFIG_FILTER = """
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>Ethernet1</name>
        <config>
            <description/>
        </config>
    </interface>
</interfaces>
"""

source = "running" tells NETCONF to retrieve the current running configuration
'''

CONFIG_FILTER = """
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>Ethernet1</name>
        <config>
            <description/>
        </config>
    </interface>
</interfaces>
"""


with connect_netconf() as conn:
    resp=conn.get_config(
    source="running",
    filter=("subtree", CONFIG_FILTER)
)

print(
    etree.tostring(
        resp.data_ele,
        pretty_print=True,
        encoding="unicode"
    )
)

'''
<data xmlns:netconf="http://arista.com/yang/rpc/netconf" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" netconf:time-modified="2026-10-21T13:19:12.692394949Z">
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name>Ethernet1</name>
      <config>
        <description>Hello World!</description>
      </config>
    </interface>
  </interfaces>
</data>

Hello World! will be returned. However, an error will occur if there is no description set.
ncclient.operations.rpc.RPCError: An unexpected element "description" is present
'''


# editing configuration

CONFIG = """

<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="http://openconfig.net/yang/interfaces">
        <interface>
            <name>Ethernet1</name>

            <config>
                <name>Ethernet1</name>
                <description>NETCONF-LAB</description>
            </config>
        </interface>
    </interfaces>
</config>
"""

with connect_netconf() as conn:
    resp = conn.edit_config(
        target="running",
        config=CONFIG,
        default_operation="merge"
    )

dom = (xml_parsing(resp.xml))

print(dom.toprettyxml())
'''
<?xml version="1.0" ?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:46514eac-aba2-40f3-9653-a1a390c92ac1">
        <ok/>
</rpc-reply>
'''

# verify if changes had been made

with connect_netconf() as conn:
    resp = conn.get_config(source="running", filter=("subtree", CONFIG_FILTER))

dom = xml_parsing(resp.data_xml)
print(dom.toprettyxml())

'''
<?xml version="1.0" ?>
<data xmlns:netconf="http://arista.com/yang/rpc/netconf" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" netconf:time-modified="2026-10-21T13:24:07.511875264Z">
        <interfaces xmlns="http://openconfig.net/yang/interfaces">
                <interface>
                        <name>Ethernet1</name>
                        <config>
                                <description>NETCONF-LAB</description>
                        </config>
                </interface>
        </interfaces>
</data>
'''