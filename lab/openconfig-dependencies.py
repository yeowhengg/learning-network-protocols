from ncclient import manager
from pathlib import Path

HOST = "172.100.100.4"

MODULES = [
    "openconfig-interfaces",
    "openconfig-yang-types",
    "openconfig-types",
    "openconfig-extensions",
    "openconfig-transport-types",
    "openconfig-hercules-interfaces",
    "openconfig-if-aggregate",
    "openconfig-if-ip",
    "openconfig-if-tunnel",
    "openconfig-vlan"
]

output_dir = Path("yang")
output_dir.mkdir(exist_ok=True)

with manager.connect(
    host=HOST,
    port=830,
    username="admin",
    password="admin",
    hostkey_verify=False,
    timeout=15
) as conn:

    for module in MODULES:
        print(f"Downloading {module}...")

        try:
            kwargs = {
                "identifier": module,
                "format": "yang",
            }

            if module == "openconfig-interfaces":
                kwargs["version"] = "2026-01-06"

            schema = conn.get_schema(**kwargs)

            filename = output_dir / f"{module}.yang"
            filename.write_text(schema.data)

            print(f"Saved: {filename}")

        except Exception as error:
            print(f"Failed to retrieve {module}: {error}")