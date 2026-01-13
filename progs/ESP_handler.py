import logging 
from pathlib import Path
import os

from html_parser import parse_ESP

logger = logging.getLogger(__name__)
class ESPHandler():
    def __init__(self, cfg, devs, service):
        self.cfg = cfg  
        self.regfile = Path(os.path.join(self.cfg['REGPath'], "regfile.yml"))        
        self.devs = devs
        self.service = service

    def query_esp(self):
        data = {}
        for dev, key in self.devs.items():
            if "shelly" not in dev.lower():
                data[dev] = parse_ESP(key[0])
                logger.debug("ESP data for %s: %s", dev, data[dev])
        return data