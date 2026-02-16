#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
import time
import logging 
import os
import threading
import asyncio
from network_scanner import NetworkScanner
import httpx

import config as config
from shelly_handler import ShellyHandler
from ESP_handler import ESPHandler
from registry import registry
from html_parser import parse_ESP

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

DISCOVERY_TIME = 5.0      # Sekunden für mDNS-Sammlung
HTTP_TIMEOUT = 5.0       # HTTP-Timeout pro Gerät

# ---------------------------------------------------------------------------
# mDNS Listener
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_devices() -> dict:
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


async def main(cfg):
    scanner = NetworkScanner(cfg)
    
    # 1. Nur die IPs holen
    print(f"--- Starte Discovery in 192.168.2.0/24 ---") #{self.target_network} 
    ips = scanner.discover_network()
    #print(f"Gefundene IPs: {ips}")

    # Hier könntest du jetzt manuell IPs hinzufügen oder entfernen
    # z.B. ips.remove("192.168.1.1") # Router ignorieren

    # 2. Die Liste abarbeiten
    if ips:
        async with httpx.AsyncClient() as client:
            tasks = [scanner.identify_device(ip, client) for ip in ips]
            devices = await asyncio.gather(*tasks)
            
            print("     Device discovery scan")
            for d in devices:
                print(f"{d['ip']:<15} | {d['Device']:<10} | {d['model']}")
        print(f"dicovered devices: {len(ips)}")

# ---------------------------------------------------------------------------
# Testlauf
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    current_file_path = os.path.realpath(__file__)
    current_file_name = os.path.basename(current_file_path)

    cfg = config.InitManager(current_file_name).ini

    asyncio.run(main(cfg))
    
"""    
    devs, service = discover_devices()
    shy = ShellyHandler(cfg, devs, service)
    esp = ESPHandler(cfg,devs, service)
    reg = registry(cfg)
    registry = reg.update_registry(devs, service)

    print(esp.query_esp())
    
    for dev, key in registry.items():
        if "shelly" in key["model"].lower():
            shelly = sh.query_shelly(key['data'][0])
            #data = shelly.read_all()
            #dev[1]["capabilities"] = shelly.get_capabilities(data)
        else:
            parse_ESP(key['data'][0])
            

    print("                                    Device discovery scan")
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
        
    #shelly = ShellyPlus4PM("192.168.2.46")
    #data = shelly.read_all()
    #pprint(data)

    #shelly1 = ShellyPlus1("192.168.2.47")
   # data1 = shelly1.read_all()
    #pprint(data1)
    
    #shelly2 = ShellyPlusPlug("192.168.2.50")
    #data2 = shelly2.read_all()
    #pprint(data)
"""