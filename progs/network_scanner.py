import logging
import asyncio
import subprocess
from scapy.all import ARP, Ether, srp
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
import httpx

logger = logging.getLogger(__name__)

class NetworkScanner:
    def __init__(self, target_network, method="ARP"):
        self.target_network = target_network
        self.active_ips = []
        self.method = method

    def discover_network(self):
        if self.method == "ARP":
            return self.discover_ips()
        elif self.method == "ZCP":
            return self.discover_zeroconf_devices()
        logger.error(f"Unbekannte Scan-Methode: {self.method}")
        return []   
        
    def discover_ips(self):
        from scapy.all import conf # Importiere die Config zum Prüfen
        logger.debug(f"DEBUG: Scapy nutzt Interface: {conf.iface}")

        arp = ARP(pdst=self.target_network)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        # 1. Warmup (fping) - Achte auf self.target_network!
        subprocess.run(["fping", "-g", self.target_network, "-a", "-q", "-r", "0"], 
                    capture_output=True)    
            
        found_ips = set()
        
        for i in range(3):
            try:
                # Sende das Paket und achte auf die Statistik
                ans, unans = srp(packet, timeout=2, verbose=True) # verbose=True zeigt Paket-Statistik!
                logger.debug(f"Versuch {i+1}: {len(ans)} Antworten erhalten.")
                
                for _, received in ans:
                    found_ips.add(received.psrc)
            except Exception as e:
                logger.error(f"Fehler: {e}")

        self.active_ips = list(found_ips)
        return self.active_ips
    def discover_zeroconf_devices() -> dict:
        logger.debug("Starting mDNS discovery")

        zeroconf = Zeroconf()
        listener = DevListener()

        ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
        time.sleep(DISCOVERY_TIME)
        zeroconf.close()

        logger.info(f"Discovery complete: {len(listener.devinfo)} devices found.")
        return listener.devinfo, listener.service

        found = {}

        for ip in listener.ips:
            result = sh._query_shelly(ip)
            if result:
                device_id, data = result
                found[device_id] = data

        logger.info("Discovery complete: %d devices found.", len(found))
        return found
    async def identify_device(self, ip, client):
        """Schritt 2: Prüft eine einzelne IP auf bekannte Profile."""
        # --- Profil: Shelly Gen 2/3 ---
        try:
            resp = await client.get(f"http://{ip}/rpc/Shelly.GetDeviceInfo", timeout=1.2)
            if resp.status_code == 200:
                data = resp.json()
                return {"ip": ip, "type": "Shelly", "gen": 2, "model": data.get("model")}
        except: pass

        # --- Profil: Shelly Gen 1 ---
        try:
            resp = await client.get(f"http://{ip}/shelly", timeout=1.0)
            if resp.status_code == 200:
                data = resp.json()
                return {"ip": ip, "type": "Shelly", "gen": 1, "model": data.get("type")}
        except: pass

        # --- Profil: WLED ---
        try:
            resp = await client.get(f"http://{ip}/json/state", timeout=1.0)
            if resp.status_code == 200:
                return {"ip": ip, "type": "WLED", "gen": "N/A", "model": "ESP-Light"}
        except: pass

        try:
            resp = await client.get(f"http://{ip}/status", timeout=1.0)
            if resp.status_code == 200:
                return {"ip": ip, "type": "ESP", "gen": "N/A", "model": "ESP-Device"}
        except: pass

        return {"ip": ip, "type": "Unbekannt", "gen": "N/A", "model": "N/A"}

    async def run_full_scan(self):
        """Koordiniert beide Schritte."""
        ips = self.discover_ips()
        if not ips:
            return []

        logger.debug(f"Identifiziere {len(ips)} Geräte...")
        async with httpx.AsyncClient() as client:
            tasks = [self.identify_device(ip, client) for ip in ips]
            return await asyncio.gather(*tasks)
        
class DevListener(ServiceListener):
    def __init__(self):
        self.devinfo = {}
        self.service = {}
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
                self.devinfo[info.server.replace(".local.", "")] = (ip, info.name)
                self.service[info.server.replace(".local.", "")] = info
                logger.info("mDNS found device at %s (%s)", ip, name)

    def update_service(self, zeroconf, service_type, name):
        logger.debug("### mDNS service updated: ### %s", name)
        pass

    def remove_service(self, zeroconf, service_type, name):
        logger.debug("### mDNS service removed ###: %s", name)
        pass
