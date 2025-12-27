"""
Shelly Registry (YAML)
=====================

- Discover Shelly devices via mDNS
- Identify devices by stable device name / ID
- Track IP changes
- Detect new and vanished devices
- Persist state to YAML
"""

from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
import requests
import threading
import time
import yaml
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------

REGISTRY_FILE = Path("shelly_registry.yml")
DISCOVERY_TIME = 5.0
HTTP_TIMEOUT = 2.0


# ---------------------------------------------------------------------------

class ShellyListener(ServiceListener):
    def __init__(self):
        self.ips = set()
        self._lock = threading.Lock()

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if not info:
            return

        addresses = info.parsed_addresses()
        if not addresses:
            return

        with self._lock:
            self.ips.add(addresses[0])

    def update_service(self, zeroconf, service_type, name):
        pass

    def remove_service(self, zeroconf, service_type, name):
        pass


# ---------------------------------------------------------------------------

def _query_shelly(ip):
    try:
        r = requests.get(f"http://{ip}/shelly", timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        data = r.json()

        name = data.get("name") or data.get("id")
        if not name:
            return None

        return name, {
            "ip": ip,
            "protocol_version": data.get("gen"),
            "last_seen": datetime.now().isoformat(timespec="seconds"),
        }

    except Exception:
        return None


# ---------------------------------------------------------------------------

def discover_devices():
    zeroconf = Zeroconf()
    listener = ShellyListener()

    ServiceBrowser(zeroconf, "_shelly._tcp.local.", listener)
    time.sleep(DISCOVERY_TIME)
    zeroconf.close()

    found = {}

    for ip in listener.ips:
        result = _query_shelly(ip)
        if result:
            name, data = result
            found[name] = data

    return found


# ---------------------------------------------------------------------------

def load_registry():
    if REGISTRY_FILE.exists():
        with REGISTRY_FILE.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
    return {}


def save_registry(registry):
    with REGISTRY_FILE.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            registry,
            f,
            sort_keys=True,
            default_flow_style=False
        )


# ---------------------------------------------------------------------------

def update_registry():
    previous = load_registry()
    current = discover_devices()

    new_devices = {}
    vanished_devices = {}
    ip_changes = {}

    for name, data in current.items():
        if name not in previous:
            new_devices[name] = data
        else:
            old_ip = previous[name].get("ip")
            if old_ip != data["ip"]:
                ip_changes[name] = {
                    "old": old_ip,
                    "new": data["ip"]
                }

    for name in previous:
        if name not in current:
            vanished_devices[name] = previous[name]

    updated_registry = previous.copy()
    updated_registry.update(current)

    save_registry(updated_registry)

    return {
        "new": new_devices,
        "vanished": vanished_devices,
        "ip_changed": ip_changes,
        "registry": updated_registry,
    }


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    result = update_registry()

    if result["new"]:
        print("Neue Geräte:")
        for name in result["new"]:
            print(f"  + {name}")

    if result["ip_changed"]:
        print("IP-Änderungen:")
        for name, change in result["ip_changed"].items():
            print(f"  * {name}: {change['old']} → {change['new']}")

    if result["vanished"]:
        print("Nicht erreichbar:")
        for name in result["vanished"]:
            print(f"  - {name}")