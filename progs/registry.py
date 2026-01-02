import logging
import yaml

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Registry I/O
# ---------------------------------------------------------------------------

class registry():
    def __init__(self, cfg):
        self.cfg = cfg  
    
    def update_registry(self, devs) -> dict:
        previous = self.load_registry()
        current = devs

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

        self.save_registry(updated)
        return updated
    
    def load_registry(self) -> dict:
        if self.cfg['REGFile'].exists():
            try:
                with self.cfg['REGFile'].open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    return data if isinstance(data, dict) else {}
            except Exception as exc:
                logger.error("Failed to load registry: %s", exc)
                return {}
        return {}


    def save_registry(self, registry: dict) -> None:
        try:
            with self.cfg['REGFile'].open("w", encoding="utf-8") as f:
                yaml.safe_dump(
                    registry,
                    f,
                    sort_keys=True,
                    default_flow_style=False
                )
        except Exception as exc:
            logger.error("Failed to save registry: %s", exc)
