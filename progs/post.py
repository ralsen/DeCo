#!/usr/bin/env python

import threading
import logging
import shared_files.config as cfg
import shared_files.DataStore as ds

import requests
import time
import socket

logger = logging.getLogger(__name__)

# The WEP_Post class is a placeholder for a post on a website.
class WEP_Post:
  def __init__(self):
    """
    The function initializes various variables and starts a thread for posting data to a web URL.
    """
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    self.sleep = cfg.ini["PostSleep"]
    self.logger = logging.getLogger(__name__)
    self.info = dict()
    self.info["name"] = socket.gethostname()
    self._post = threading.Thread(target=self._postit, daemon=True).start()
    ds.put("System", ("starttime_app", int(time.time())))
    self.logger.info("Client posting started, sending to: " + cfg.ini['web_URL'])
    self.repError = False

  def _postit(self):
    """
    The function `_postit` sends data to a server at regular intervals, rounding the values and
    handling any errors that occur.
    """
    while True:
        for x in ds.DS.ds['WEB']:
          if x != "Commons":
            value = ds.DS.ds['WEB'][x]['CURRENT_DATA']
            try:
              resstr = str(round(value, 2))
            except:
              resstr = str(value)
            self.info[x] = resstr

        try:
          #logger.info(f"{ds.DS.ds['EDAG_P_SIM_TX_3']}")
          #logger.info(f"{self.info}")
          response = requests.post(f"{cfg.ini['web_URL']}/", json=self.info)
          if self.repError:
            self.logger.info("send to server resumed.")
            self.repError = False
        except:
          if not self.repError:
            self.logger.error("could not post to server!!!")
            self.repError = True
        time.sleep(self.sleep)
