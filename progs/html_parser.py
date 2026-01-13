import requests
import re
import logging
from pathlib import Path
import os

logger = logging.getLogger(__name__)

def parse_ESP(ip):    
    try:
        html = requests.get(f"http://{ip}").text
    except Exception as exc:
        logger.error("Fehler beim Abrufen der HTML-Seite von %s: %s", ip, exc)
        return {}

    # Extrahiere nur den Inhalt zwischen <div1> und </div1>
    div1_content = re.search(r'<div1>(.*?)</div1>', html, re.DOTALL).group(1)

    # Extrahiere alle Schlüssel-Wert-Paare, ignoriere leere Zeilen und <br>-Tags
    matches2 = re.findall(r'([^:<]+):\s*([^<]+)', div1_content)
    data = {key: value for key, value in matches2}

    data_dict = {}
    for key, value in data.items():
        if key.startswith("/h3>\r\n-----> "):
            cleaned_key = key.split("V", 1)[-1]
            version = cleaned_key.split(" ", 1)[0]
            data_dict["Version"] = f"V{version}"
        else:
            data_dict[key.split(">")[-1]] = value.strip()

    try:
        data_dict["Hostname"]
    except KeyError:
        data_dict["Hostname"] = "ESP_Device ohne Hostname"

    hostfile = Path(os.path.join("/Users/ralphfollrichs/Projects/DeCo/progs/../reg/", f"{data_dict['Hostname']}.yml"))
    with open(hostfile, 'w') as f:
        for key, value in data_dict.items():
            f.write(f"{key}: {value}\n")

    logger.debug(f"Daten wurden in {hostfile} geschrieben.")
    return data_dict
