#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
import time
import logging 
import os
import threading


import config
from shelly_handler import ShellyHandler
from registry import registry


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

DISCOVERY_TIME = 5.0      # Sekunden für mDNS-Sammlung
HTTP_TIMEOUT = 2.0       # HTTP-Timeout pro Gerät

# ---------------------------------------------------------------------------
# mDNS Listener
# ---------------------------------------------------------------------------

class DevListener(ServiceListener):
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

    found = {}

    for ip in listener.ips:
        result = sh._query_shelly(ip)
        if result:
            device_id, data = result
            found[device_id] = data

    logger.info("Discovery complete: %d devices found.", len(found))
    return found

# ---------------------------------------------------------------------------
# Testlauf
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    current_file_path = os.path.realpath(__file__)
    current_file_name = os.path.basename(current_file_path)

    cfg = config.InitManager(current_file_name).ini

    sh = ShellyHandler(cfg)
    reg = registry(cfg)
    devs = discover_devices()
    registry = reg.update_registry(devs)

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