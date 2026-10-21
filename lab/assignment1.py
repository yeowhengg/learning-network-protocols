from netconf_reusable import connect_netconf, xml_parsing

#-------------------------------TASK 1----------------------------------------------------
IDENTIFIER = "openconfig-interfaces"
# learn how to query and find for modules
with connect_netconf() as conn:
    for cap in conn.server_capabilities:
        if "interface" in cap:
            print(cap)


    schema = conn.get_schema(
        identifier = f"{IDENTIFIER}",
        format="yang"
    )

    with open(f"{IDENTIFIER}.yang", "w") as file:
        file.write(schema.data)

    print("schema saved")

'''
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
'''

"""
i need the following data:

1. interface name
2. administrative status
3. operational status
4. mtu
5. interface description

translates to:
1. /interfaces/interface[name=Ethernet1]/state/name
2. /interfaces/interface[name=Ethernet1]/state/admin-status
3. /interfaces/interface[name=Ethernet1]/state/oper-status
4. /interfaces/interface[name=Ethernet1]/state/mtu
5. /interfaces/interface[name=Ethernet1]/state/description

"""

FILTER = """

<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>Ethernet1</name>
        <state>
            <name/>
            <admin-status/>
            <oper-status/>
            <mtu/>
            <description/>
        </state>
    </interface>
</interfaces>
"""

with connect_netconf() as conn:
    resp = conn.get(filter=("subtree", FILTER))

dom = xml_parsing(resp.data_xml)
print(dom.toprettyxml())

#-----------------------------END OF TASK 1------------------------------

#----------------------------TASK 2 reusable interface name------------------------------



def get_interface_status(interface_name: str) -> str | None:
    FILTER = f"""
    <interfaces xmlns="http://openconfig.net/yang/interfaces">
        <interface>
            <name>{interface_name}</name>
            <state>
                <oper-status/>
            </state>
        </interface>
    </interfaces>
    """

    with connect_netconf() as conn:
        resp = conn.get(filter=("subtree",FILTER))
    dom = xml_parsing(resp.data_xml)
    return dom.toprettyxml()

print("interface retrieved: ", get_interface_status("Ethernet1"))
print("interface retrieved: ", get_interface_status("Ethernet2"))


#-------------------------END OF TASK 2-----------------------------

#--------------------------TASK 3----------------------------------

FILTER = """
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>Ethernet1</name>
        <config/>
    </interface>
</interfaces>
"""

with connect_netconf() as conn:
    resp = conn.get_config(
        source="running",
        filter=("subtree", FILTER)
    )

    print(xml_parsing(resp.data_xml).toprettyxml())

GET_FILTER = f"""
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>Ethernet1</name>
        <state>
            <admin-status/>
            <oper-status/>
        </state>
    </interface>
</interfaces>
"""

with connect_netconf() as conn:
    resp = conn.get(filter=("subtree", GET_FILTER))
    print(xml_parsing(resp.data_xml).toprettyxml())

GET_CONF_FILTER = """
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
    resp = conn.get_config(source="running", filter=("subtree", GET_CONF_FILTER))
    print(xml_parsing(resp.data_xml).toprettyxml())
    print("hello")

