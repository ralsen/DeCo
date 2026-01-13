import logging
import yaml
import time
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Registry I/O
# ---------------------------------------------------------------------------

class registry():
    def __init__(self, cfg):
        self.cfg = cfg  
        self.regfile = Path(os.path.join(self.cfg['REGPath'], "regfile.yml"))
        print(f"Registry file path: {self.regfile}") 
    def update_registry(self, devs, service) -> dict:
        previous = self.load_registry()
        current = devs
        updated = previous.copy()
        
        for dev in updated.values():
            dev["present"] = False

        #updated = {}
        for device_id, data in current.items():
            if device_id not in updated:
                updated[device_id] = {}
                updated[device_id]["data"] = data
                updated[device_id]['model'] = data[1]   
                logger.debug("New device discovered: %s", device_id)
            else:
                updated[device_id].update(data)

            updated[device_id]['present'] = True
            updated[device_id]["last_seen"] = int(time.time())

        self.save_registry(updated)
        return updated
    
    def load_registry(self) -> dict:
        if self.regfile.exists():
            try:
                with self.regfile.open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    return data if isinstance(data, dict) else {}
            except Exception as exc:
                logger.error("Failed to load registry: %s", exc)
                return {}
        return {}


    def save_registry(self, registry: dict) -> None:
        try:
            with self.regfile.open("w", encoding="utf-8") as f:
                yaml.safe_dump(
                    registry,
                    f,
                    sort_keys=True,
                    default_flow_style=False,
                    allow_unicode=True 
                )
        except Exception as exc:
            logger.error("Failed to save registry: %s", exc, device_id)
