"""
Shelly Registry (YAML)
=====================

- Discover Shelly devices via mDNS
- Stable device identity (device ID / name)
- Honest data model:
    * family   = physical product (model)
    * role     = configured operating mode (type)
    * category = optional heuristic grouping
- Persist all available device information
- Track presence state
"""

from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
import requests
import threading
import time
import yaml
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

REGISTRY_FILE = Path("shelly_registry.yml")
DISCOVERY_TIME = 5.0      # Sekunden für mDNS-Sammlung
HTTP_TIMEOUT = 2.0       # HTTP-Timeout pro Gerät


# ---------------------------------------------------------------------------
# mDNS Listener
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
# Ehrliche Ableitungen
# ---------------------------------------------------------------------------

def get_family(data: dict) -> str:
    """Physisches Produkt (stabil)"""
    return data.get("model") or "Unknown"


def get_role(data: dict) -> str:
    """Aktuelle Betriebsart (konfigurationsabhängig)"""
    return data.get("type") or "Unknown"


def derive_category(data: dict) -> str:
    """
    Optionale Gruppierung.
    Darf 'Unknown' sein – keine Garantie!
    """
    model = (data.get("model") or "").upper()
    role = (data.get("type") or "").upper()

    if role == "COVER":
        return "Cover"

    if "PLUG" in model:
        return "Plug"

    if "EM" in model:
        return "EM"

    if model.startswith("SHELLYPRO"):
        return "Pro"

    return "Unknown"


# ---------------------------------------------------------------------------
# Einzelgerät abfragen
# ---------------------------------------------------------------------------

def _query_shelly(ip: str):
    try:
        r = requests.get(f"http://{ip}/shelly", timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        data = r.json()

        device_id = data.get("name") or data.get("id")
        if not device_id:
            return None

        now = datetime.now().isoformat(timespec="seconds")

        return device_id, {
            "id": data.get("id"),
            "name": data.get("name"),
            "model": data.get("model"),
            "family": get_family(data),
            "role": get_role(data),
            "category": derive_category(data),
            "mac": data.get("mac"),
            "ip": ip,
            "protocol_version": data.get("gen"),
            "firmware": data.get("ver"),
            "firmware_id": data.get("fw_id"),
            "present": True,
            "last_seen": now,
        }

    except Exception:
        return None


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_devices() -> dict:
    zeroconf = Zeroconf()
    listener = ShellyListener()

    ServiceBrowser(zeroconf, "_shelly._tcp.local.", listener)
    time.sleep(DISCOVERY_TIME)
    zeroconf.close()

    found = {}

    for ip in listener.ips:
        result = _query_shelly(ip)
        if result:
            device_id, data = result
            found[device_id] = data

    return found


# ---------------------------------------------------------------------------
# Registry I/O
# ---------------------------------------------------------------------------

def load_registry() -> dict:
    if REGISTRY_FILE.exists():
        with REGISTRY_FILE.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
    return {}


def save_registry(registry: dict) -> None:
    with REGISTRY_FILE.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            registry,
            f,
            sort_keys=True,
            default_flow_style=False
        )


# ---------------------------------------------------------------------------
# Registry Update
# ---------------------------------------------------------------------------

def update_registry() -> dict:
    previous = load_registry()
    current = discover_devices()

    updated = previous.copy()

    # alle bekannten Geräte zunächst als nicht präsent markieren
    for dev in updated.values():
        dev["present"] = False

    # aktuelle Geräte einpflegen
    for device_id, data in current.items():
        if device_id not in updated:
            updated[device_id] = data
        else:
            updated[device_id].update(data)

        updated[device_id]["present"] = True
        updated[device_id]["last_seen"] = data["last_seen"]

    save_registry(updated)
    return updated


# ---------------------------------------------------------------------------
# Testlauf
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    registry = update_registry()

    for name, dev in registry.items():
        state = "online" if dev["present"] else "offline"
        print(
            f"{name:35} "
            f"{state:7} "
            f"{dev['family']:20} "
            f"{dev['role']:8} "
            f"{dev['category']}"
        )
        
# state (online) ist scheinbar nicht für jedes gerät sondern "ein" globaler zustand        
# role und category sind immer "unknown"