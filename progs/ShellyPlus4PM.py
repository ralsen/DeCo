import requests
from typing import Dict, Any


class ShellyPlus4PM:
    """
    Liest alle relevanten Daten eines Shelly Plus 4PM (S4PL-00416EU)
    und gibt sie als Dictionary zurück.
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
        """
        Liest alle verfügbaren Daten und fasst sie in einem Dictionary zusammen.
        """
        data = {
            "device_info": {},
            "status": {},
            "config": {},
            "meters": {},
            "switches": {}
        }

        data["device_info"] = self.get_device_info()
        status = self.get_status()
        data["status"] = status
        data["config"] = self.get_config()

        # Leistungsdaten (integrierte PMs)
        for key, value in status.items():
            if key.startswith("switch:"):
                idx = key.split(":")[1]
                data["switches"][idx] = {
                    "output": value.get("output"),
                    "apower": value.get("apower"),
                    "voltage": value.get("voltage"),
                    "current": value.get("current"),
                    "aenergy": value.get("aenergy"),
                    "temperature": value.get("temperature"),
                }

        return data