import asyncio
import subprocess
from scapy.all import ARP, Ether, srp

class NetworkScanner:
    def __init__(self, target_network):
        self.target_network = target_network
        self.active_ips = []

    def discover_ips(self):
        """Schritt 1: Findet alle aktiven IPs im Netzwerk via ARP."""
        print(f"--- Starte Discovery in {self.target_network} ---")
        arp = ARP(pdst=self.target_network)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        cmd = ["fping", "-g", "192.168.2.0/24", "-a", "-q", "-r", "0"]
        subprocess.run(cmd, capture_output=True, timeout=5)    
            
        for i in range(3):
            try:
                # Sende Broadcast und sammle Antworten
                result = srp(packet, timeout=2, verbose=False)[0]
                self.active_ips = [received.psrc for sent, received in result]
                return self.active_ips
            except PermissionError:
                print("ERROR: Admin-Rechte erforderlich!")
                return []

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
                #print(resp.text)
                return {"ip": ip, "type": "ESP", "gen": "N/A", "model": "ESP-Device"}
        except: pass

        return {"ip": ip, "type": "Unbekannt", "gen": "N/A", "model": "N/A"}

    async def run_full_scan(self):
        """Koordiniert beide Schritte."""
        ips = self.discover_ips()
        if not ips:
            return []

        print(f"Identifiziere {len(ips)} Geräte...")
        async with httpx.AsyncClient() as client:
            tasks = [self.identify_device(ip, client) for ip in ips]
            return await asyncio.gather(*tasks)