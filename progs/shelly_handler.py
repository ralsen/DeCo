import logging
import requests
import json
import time
from datetime import datetime


from datetime import datetime 

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

DISCOVERY_TIME = 5.0      # Sekunden für mDNS-Sammlung
HTTP_TIMEOUT = 2.0       # HTTP-Timeout pro Gerät

# ---------------------------------------------------------------------------
# Fähigkeits-Erkennung (klassisch: was antwortet, ist da)
# ---------------------------------------------------------------------------

class ShellyHandler():
    def __init__(self, cfg):
        self.cfg = cfg  

    def _query_shelly(self, ip: str):
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
            caps = self.detect_capabilities(ip)
            caps = "capas"
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
                #"category": self.derive_category_from_caps(caps),
                "present": True,
                "last_seen": now,
            }

        except Exception as exc:
            logger.warning("Failed to query Shelly at %s: %s", ip, exc)
            return None
    def _has_rpc(self, ip: str, method: str) -> bool:
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


    def detect_capabilities(self, ip: str) -> list[str]:
        caps = []

        if self._has_rpc(ip, "Switch.GetConfig"):
            caps.append("relay")

        elif self._has_rpc(ip, "Cover.GetConfig"):
            caps.append("cover")

        elif self._has_rpc(ip, "EM.GetConfig"):
            caps.append("em")

        elif self._has_rpc(ip, "PM1.GetConfig"):
            caps.append("power_meter")

        elif self._has_rpc(ip, "Input.GetConfig"):
            caps.append("input")
            
        else:
            caps.append("generic")
        logger.debug("Capabilities for %s: %s", ip, caps)
        return caps


    def derive_category_from_caps(self, caps: list[str]) -> str:
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

