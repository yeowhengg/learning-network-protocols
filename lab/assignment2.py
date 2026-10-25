from netconf_reusable import connect_netconf, xml_parsing
import xml.etree.ElementTree as ET
import urllib.parse
#----------TASK 1-----------------

def parse_yang_capabilities(capabilities):
    parsed = urllib.parse.urlsplit(capabilities)
    query = urllib.parse.parse_qs(parsed.query)

    module = query.get("module", [None])[0]
    if module is None:
        return None
    revision = query.get("revision", [None])[0]
    #print(parsed.scheme, parsed.netloc, parsed.path) # http arista.com /yang/openconfig/deviations/dev-mod-2
    namespace = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", "")) #http://arista.com/yang/openconfig/deviations/dev-mod-1
    category = get_native_or_vendor_module(module)

    return module, category, revision, namespace

def get_native_or_vendor_module(module: str) -> str | None:
    if module.startswith("openconfig"):
        return "OpenConfig"
    elif module.startswith("arista"):
        if "deviation" in module:
            return "Arista Deviation"
        elif "augments" in module:
            return "Arista Augmentation"
        else:
            return "Arista Native"
    else:
        return "Others"

print("YANG CAPABILITY DISCOVERY")
with connect_netconf() as conn:
    for cap in conn.server_capabilities:
        parsed = parse_yang_capabilities(cap)
        module = category = revision = namespace = None
        if parsed is None:
            continue

        module, category, revision, namespace = parsed
        print(f"Module: {module}\nCategory: {category}\nRevision: {revision}\nNamespace: {namespace}\n")   

assert get_native_or_vendor_module("openconfig-interfaces") == "OpenConfig"
assert get_native_or_vendor_module("arista-intf-augments") == "Arista Augmentation"
test_capability = (
    "http://arista.com/yang/openconfig/interfaces/augments"
    "?module=arista-intf-augments&revision=2026-01-14"
)

result = parse_yang_capabilities(test_capability)

print(result)
#-----------------------------END OF TASK 1----------------

#-----------------------------TASK 2-----------------------------

# Task A
schema = None
with connect_netconf() as conn:
    for cap in conn.server_capabilities:
        if "arista.com/yang/openconfig/interfaces" in cap:
            print(cap) # http://arista.com/yang/openconfig/interfaces/augments?module=arista-intf-augments&revision=2026-01-14

    schema = conn.get_schema("arista-intf-augments", "yang").data
print(type(schema))
with open ("arista-intf-augments.yang", "w") as f:
    f.write(schema)

# Task B
# 1. get state/oper-status of interface Ethernet1
# 2. get Arista-specific state / inactive of interface Ethernet1

FILTER_OPER_STATUS = """
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>Ethernet1</name>
        <state>
            <oper-status/>
        </state>
    </interface>
</interfaces>
"""

FILTER_AUGMENTATION = """
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>Ethernet1</name>
        <state>
            <inactive xmlns="http://arista.com/yang/openconfig/interfaces/augments"/>
        </state>
    </interface>
</interfaces>
"""

# ^ the above is correct, but in netconf, we can combine them together in same namespace.
# since the augmentation is in the same namespace as OC, and its only being extended, we can combine them together
COMBINED_FILTER = """
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>Ethernet1</name>
        <state>
            <oper-status/>
            <inactive xmlns="http://arista.com/yang/openconfig/interfaces/augments"/>
        </state>
    </interface>
</interfaces>
"""

oper_status_resp = augmentation_resp = None
with connect_netconf() as conn:
    oper_status_resp = conn.get(filter=("subtree", FILTER_OPER_STATUS))
    augmentation_resp = conn.get(filter=("subtree", FILTER_AUGMENTATION))
    combined_resp = conn.get(filter=("subtree", COMBINED_FILTER))

    print("OPER-STATUS RESPONSE")
    print(oper_status_resp)
    print("AUGMENTATION RESPONSE")
    print(augmentation_resp)
    print("COMBINED RESPONSE")
    print(combined_resp)

oper_status_root = ET.fromstring(oper_status_resp.data_xml)
augmentation_root = ET.fromstring(augmentation_resp.data_xml)
combined_root = ET.fromstring(combined_resp.data_xml)

namespace = {
    "oc": "http://openconfig.net/yang/interfaces",
    "arista": "http://arista.com/yang/openconfig/interfaces/augments",
}

oper_status_interface = oper_status_root.find(".//oc:interface", namespace)
augmentation_interface = augmentation_root.find(".//oc:interface", namespace)
combined_interface = combined_root.find(".//oc:interface", namespace)

oper_status = oper_status_interface.find(".//oc:oper-status", namespace).text if oper_status_interface is not None else None
augmentation_inactive = augmentation_interface.find(".//arista:inactive", namespace).text if augmentation_interface is not None else None
print(oper_status, augmentation_inactive)

combined_oper_status = combined_interface.find(".//oc:oper-status", namespace).text if combined_interface is not None else None
combined_augmentation_inactive = combined_interface.find(".//arista:inactive", namespace).text if combined_interface is not None else None
print(combined_oper_status, combined_augmentation_inactive)

#-----------------------------END OF TASK 2----------------

#-----------------------------TASK 3-----------------------------
'''
Scenario
Your cEOS previously advertised arista-interfaces-notsupported-deviations. That module contains deviation
statements with deviate not-supported. Your task is to build an evidence-based inventory of those paths.
Exercise A — Deviation inventory (15 marks)
• Retrieve and save the device-advertised deviation YANG module and record its revision.
• Find the targeted YANG paths and the operation specified by each deviation.
• Count not-supported declarations dynamically; do not hardcode the count.
• Display at least five exact deviation paths, including tunnel-related paths if they exist in the retrieved module.
• Explain whether you used a YANG parser or a preliminary text-matching method. Explain how text matching
could fail on complex YANG syntax.
'''

print("DEVIATION YANG MODULE and REVISIONS")
deviation_count = 0
deviation_list = []
with connect_netconf() as conn:
    for cap in conn.server_capabilities:
        if "deviation" in cap:
            parsed = parse_yang_capabilities(cap)
            module = category = revision = namespace = None
            if parsed is None:
                continue

            module, category, revision, namespace = parsed
            deviation_count += 1
            print(f"Module: {module}\nCategory: {category}\nRevision: {revision}\nNamespace: {namespace}\n")   

def store_tunnel_deviation_modules(module):
    pass