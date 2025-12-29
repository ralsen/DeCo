import requests
from typing import Dict, Any


class ShellyPlusPlug:
    """
    Liest alle relevanten Daten eines Shelly Plus Plug
    (SNPL-00112EU) über die RPC-API
    """

    def __init__(self, ip_address: str, timeout: float = 5.0):
        self.ip = ip_address
        self.base_url = f"http://{self.ip}"
        self.timeout = timeout

    def _get(self, path: str) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_device_info(self) -> Dict[str, Any]:
        return self._get("/rpc/Shelly.GetDeviceInfo")

    def get_status(self) -> Dict[str, Any]:
        return self._get("/rpc/Shelly.GetStatus")

    def get_config(self) -> Dict[str, Any]:
        return self._get("/rpc/Shelly.GetConfig")

    def read_all(self) -> Dict[str, Any]:
        status = self.get_status()
        switch = status.get("switch:0", {})

        return {
            "device_info": self.get_device_info(),
            "switch": {
                "output": switch.get("output"),
                "apower": switch.get("apower"),
                "voltage": switch.get("voltage"),
                "current": switch.get("current"),
                "aenergy": switch.get("aenergy"),
                "temperature": switch.get("temperature"),
            },
            "wifi": status.get("wifi"),
            "cloud": status.get("cloud"),
            "system": status.get("sys"),
            "config": self.get_config(),
        }