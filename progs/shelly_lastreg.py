#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import socket
import logging
import requests
from zeroconf import Zeroconf, ServiceBrowser

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# ---------------------------------------------------------------------------
# RPC helper
# ---------------------------------------------------------------------------

def rpc_call(ip, method, params=None, timeout=3):
    payload = {
        "id": 1,
        "method": method,
    }
    if params:
        payload["params"] = params

    url = "http://{}/rpc".format(ip)
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()

    data = r.json()
    if "error" in data:
        raise RuntimeError(data["error"])

    return data.get("result", {})


# ---------------------------------------------------------------------------
# Capability detection (entscheidend!)
# ---------------------------------------------------------------------------

def detect_capabilities(ip, logger):
    capabilities = []

    probes = {
        "switch": "Switch.GetStatus",
        "light":  "Light.GetStatus",
        "input":  "Input.GetStatus",
        "script": "Script.List",
    }

    for cap, method in probes.items():
        try:
            rpc_call(ip, method)
            capabilities.append(cap)
        except Exception:
            pass

    # Meter ist historisch Teil von Switch
    if "switch" in capabilities:
        try:
            st = rpc_call(ip, "Switch.GetStatus")
            if "apower" in st or "aenergy" in st:
                capabilities.append("meter")
        except Exception:
            pass

    return sorted(set(capabilities))


# ---------------------------------------------------------------------------
# Kategorieableitung (klassisch, deterministisch)
# ---------------------------------------------------------------------------

def categorize_device(capabilities):
    caps = set(capabilities)

    if "light" in caps:
        return "Light"
    if "switch" in caps and "meter" in caps:
        return "PowerSwitch"
    if "switch" in caps:
        return "Switch"
    return "Generic"


# ---------------------------------------------------------------------------
# Device identity
# ---------------------------------------------------------------------------

def get_device_identity(ip):
    info = rpc_call(ip, "Shelly.GetDeviceInfo")

    return {
        "mac": info.get("mac"),
        "model": info.get("type"),
        "name": info.get("name") or info.get("id") or info.get("mac"),
        "fw": info.get("fw"),
    }


# ---------------------------------------------------------------------------
# Zeroconf listener
# ---------------------------------------------------------------------------

class ShellyListener:
    def __init__(self):
        self.found_ips = set()

    def add_service(self, zeroconf, service_type, name):
        try:
            info = zeroconf.get_service_info(service_type, name)
            if not info or not info.addresses:
                return

            ip = socket.inet_ntoa(info.addresses[0])
            self.found_ips.add(ip)

            logger.debug("zeroconf: %s -> %s", name, ip)

        except Exception as e:
            logger.debug("zeroconf error: %s", e)

    def remove_service(self, zeroconf, service_type, name):
        pass


# ---------------------------------------------------------------------------
# Registry handling
# ---------------------------------------------------------------------------

def update_registry(registry, ip, logger):
    try:
        ident = get_device_identity(ip)
    except Exception as e:
        logger.warning("%s: no Shelly RPC (%s)", ip, e)
        return

    mac = ident.get("mac")
    if not mac:
        logger.warning("%s: missing MAC", ip)
        return

    dev = registry.setdefault(mac, {})

    dev["ip"] = ip
    dev["model"] = ident.get("model", "unknown")
    dev["name"] = ident.get("name", mac)
    dev["fw"] = ident.get("fw")
    dev["present"] = True
    dev["last_seen"] = time.time()

    caps = detect_capabilities(ip, logger)
    dev["capabilities"] = caps
    dev["category"] = categorize_device(caps)

    logger.debug(
        "registered %s (%s) caps=%s",
        dev["name"], mac, ",".join(caps)
    )


def mark_offline_devices(registry, max_age=30):
    now = time.time()
    for dev in registry.values():
        if now - dev.get("last_seen", 0) > max_age:
            dev["present"] = False


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_registry(registry):
    print(
        "{:<35} {:<7} {:<18} {:<25} {}".format(
            "Name", "State", "Model", "Capabilities", "Category"
        )
    )
    print("-" * 100)

    for dev in registry.values():
        state = "online" if dev.get("present") else "offline"
        caps = ",".join(dev.get("capabilities", []))

        print(
            "{:<35} {:<7} {:<18} {:<25} {}".format(
                dev.get("name", ""),
                state,
                dev.get("model", ""),
                caps,
                dev.get("category", ""),
            )
        )

    print("-" * 100)


# ---------------------------------------------------------------------------
# Main discovery loop
# ---------------------------------------------------------------------------

def discover_shellys(timeout=5):
    zeroconf = Zeroconf()
    listener = ShellyListener()

    ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    time.sleep(timeout)
    zeroconf.close()

    return listener.found_ips


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    registry = {}

    ips = discover_shellys(timeout=5)
    logger.info("found %d IPs", len(ips))

    for ip in ips:
        update_registry(registry, ip, logger)

    mark_offline_devices(registry)
    print_registry(registry)