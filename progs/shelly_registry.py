"""
Shelly Registry (YAML)
=====================

- Discover Shelly devices via mDNS (_shelly._tcp.local.)
- Stable device identity (device ID / name)
- Classification by capabilities (not roles, not marketing)
- Persist all available device information
- Track presence state
"""

from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
import requests
import threading
import time
import logging
import yaml
import os
from datetime import datetime
from pprint import pprint


import progs.config as config
from registry import registry as reg
from ShellyPlus4PM import ShellyPlus4PM
from ShellyPlus1 import ShellyPlus1
from ShellyPlusPlug import ShellyPlusPlug

logger = logging.getLogger(__name__)
logging.getLogger('urllib3').setLevel(logging.WARNING)


# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

#cfg['REGFile'] = Path("shelly_registry.yml")
DISCOVERY_TIME = 5.0      # Sekunden für mDNS-Sammlung
HTTP_TIMEOUT = 2.0       # HTTP-Timeout pro Gerät


# ---------------------------------------------------------------------------
# mDNS Listener (nur Shelly-Services!)
# ---------------------------------------------------------------------------

class ShellyListener(ServiceListener):
    def __init__(self):
        self.ips = set()
        self._lock = threading.Lock()

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if info:
            if not info:
                logger.debug("mDNS service without info: %s", name)
                return

            addresses = info.parsed_addresses()
            if not addresses:
                logger.debug("mDNS service without address: %s", name)
                return

            with self._lock:
                ip = addresses[0]
                self.ips.add(ip)
                logger.info("mDNS found Shelly at %s (%s)", ip, name)

    def update_service(self, zeroconf, service_type, name):
        logger.debug("### mDNS service updated: ### %s", name)
        pass

    def remove_service(self, zeroconf, service_type, name):
        logger.debug("### mDNS service removed ###: %s", name)
        pass


# ---------------------------------------------------------------------------
# Fähigkeits-Erkennung (klassisch: was antwortet, ist da)
# ---------------------------------------------------------------------------

def _has_rpc(ip: str, method: str) -> bool:
    try:
        r = requests.post(
            f"http://{ip}/rpc/{method}",
            json={},
            timeout=HTTP_TIMEOUT
        )
        logger.debug("RPC %s on %s -> %s", method, ip, r.status_code)        
        return r.status_code == 200
    except Exception as exc:
        logger.debug("RPC %s on %s failed: %s", method, ip, exc)        
        return False


def detect_capabilities(ip: str) -> list[str]:
    caps = []

    if _has_rpc(ip, "Switch.GetConfig"):
        caps.append("relay")

    elif _has_rpc(ip, "Cover.GetConfig"):
        caps.append("cover")

    elif _has_rpc(ip, "EM.GetConfig"):
        caps.append("em")

    elif _has_rpc(ip, "PM1.GetConfig"):
        caps.append("power_meter")

    elif _has_rpc(ip, "Input.GetConfig"):
        caps.append("input")
        
    else:
        caps.append("generic")
    logger.debug("Capabilities for %s: %s", ip, caps)
    return caps


def derive_category_from_caps(caps: list[str]) -> str:
    """
    Optionale Komfort-Gruppierung.
    Kein Fakt, nur Ableitung.
    """
    if "cover" in caps:
        return "Cover"
    if "em" in caps:
        return "EM"
    if "relay" in caps and "power_meter" in caps:
        return "Plug"
    return "Generic"


# ---------------------------------------------------------------------------
# Einzelgerät abfragen
# ---------------------------------------------------------------------------

def _query_shelly(ip: str):
    try:
        logger.debug("Query Shelly at %s", ip)
        
        r = requests.get(f"http://{ip}/shelly", timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        data = r.json()

        device_id = data.get("name") or data.get("id")
        if not device_id:
            logger.warning("Shelly at %s returned no id/name", ip)
            return None

        now = datetime.now().isoformat(timespec="seconds")
        caps = detect_capabilities(ip)

        return device_id, {
            "id": data.get("id"),
            "name": data.get("name"),
            "model": data.get("model"),
            "gen": data.get("gen"),
            "mac": data.get("mac"),
            "ip": ip,
            "protocol_version": data.get("gen"),
            "firmware": data.get("ver"),
            "firmware_id": data.get("fw_id"),
            "capabilities": caps,
            "category": derive_category_from_caps(caps),
            "present": True,
            "last_seen": now,
        }

    except Exception as exc:
        logger.warning("Failed to query Shelly at %s: %s", ip, exc)
        return None


# ---------------------------------------------------------------------------
# Discovery (ausschließlich Shelly-mDNS)
# ---------------------------------------------------------------------------

def discover_devices() -> dict:
    logger.debug("Starting mDNS discovery")

    zeroconf = Zeroconf()
    listener = ShellyListener()

    ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    time.sleep(DISCOVERY_TIME)
    zeroconf.close()

    found = {}

    for ip in listener.ips:
        result = _query_shelly(ip)
        if result:
            device_id, data = result
            found[device_id] = data

    logger.info("Discovery complete: %d devices found.", len(found))
    return found


# ---------------------------------------------------------------------------
# Registry I/O
# ---------------------------------------------------------------------------

def load_registry() -> dict:
    if cfg['REGFile'].exists():
        try:
            with cfg['REGFile'].open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data if isinstance(data, dict) else {}
        except Exception as exc:
            logger.error("Failed to load registry: %s", exc)
            return {}
    return {}


def save_registry(registry: dict) -> None:
    try:
        with cfg['REGFile'].open("w", encoding="utf-8") as f:
            yaml.safe_dump(
                registry,
                f,
                sort_keys=True,
                default_flow_style=False
            )
    except Exception as exc:
        logger.error("Failed to save registry: %s", exc)


# ---------------------------------------------------------------------------
# Registry Update
# ---------------------------------------------------------------------------

def update_registry() -> dict:
    previous = load_registry()
    current = discover_devices()

    updated = previous.copy()

    for dev in updated.values():
        dev["present"] = False

    for device_id, data in current.items():
        if device_id not in updated:
            updated[device_id] = data
            logger.debug("New device discovered: %s", device_id)
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
    current_file_path = os.path.realpath(__file__)
    current_file_name = os.path.basename(current_file_path)

    cfg = config.InitManager(current_file_name).ini

    registry = update_registry()

    print("                                    Shelly discovery scan")
    print("Name                                State   Model                Capabilities             Category")
    print("--------------------------------------------------------------------------------------------------")

    for name, dev in registry.items():
        state = "online" if dev["present"] else "offline"
        caps = ",".join(dev.get("capabilities", []))
        print(
            f"{name:35} "
            f"{state:7} "
            f"{dev.get('model', ''):20} "
            f"{caps:25} "
            f"{dev.get('category')}"
        )
        
    shelly = ShellyPlus4PM("192.168.2.46")
    data = shelly.read_all()
    #pprint(data)

    shelly1 = ShellyPlus1("192.168.2.47")
    data1 = shelly1.read_all()
    #pprint(data1)
    
    shelly2 = ShellyPlusPlug("192.168.2.50")
    data2 = shelly2.read_all()
    #pprint(data)