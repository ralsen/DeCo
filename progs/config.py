#!/usr/bin/env python3 xxx
# -*- coding: utf-8 -*-
import logging
import yaml
import socket
import datetime
import os
import time
from pathlib import Path
import platform

from threadmanager import ThreadManager

logger = logging.getLogger(__name__)

class InitManager:
    def __init__(self, progname: str):
        self.ini = {}
        self.progname = progname
        self.load_init()
        
    def get_external_ip(self) -> str:
        try:
            # create a dummy socket to determine the external IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Google DNS as target
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        
        except Exception as e:
            return f"Fehler: {e}"

    def load_init(self):
        current_dir = os.getcwd()
        current_dir += '/..'
        with open(f'{current_dir}/yml/config.yml', 'r') as ymlfile:
            confyml = yaml.safe_load(ymlfile)

        RootPath = current_dir #confyml['ROOT_PATH']
        ini = self.ini
        ini['StartTime'] = datetime.datetime.now()
        ini['confyml'] = confyml
        ini['LogPath'] = RootPath + confyml['pathes']['LOG']
        ini['DataPath'] = RootPath + confyml['pathes']['DATA']
        ini['RRDPath'] = RootPath + confyml['pathes']['RRD']
        ini['YMLPath'] = RootPath + confyml['pathes']['YML']
        ini['PNGPath'] = RootPath + confyml['pathes']['PNG']
        ini['REGPath'] = RootPath + confyml['pathes']['REG']
        #ini['REGFile'] = Path(RootPath + confyml['pathes']['REG'])
        ini['DeSePort'] = confyml['Communication']['DevServerPort']
        ini['DeSeName'] = confyml['Communication']['DevServerName']
        ini['debugdatefmt'] = confyml['debug']['datefmt']
        ini['logSuffix'] = confyml['suffixes']['log']
        ini['dataSuffix'] = confyml['suffixes']['data']
        ini['hirestime'] = confyml['debug']['hirestime']
        ini['SystemMonitorSleep'] = confyml['Timers']['SystemMonitorSleep']
        ini['mainloop_sleep'] = confyml['Timers']['mainloop_sleep']
        ini['humanTimestamp'] = confyml['misc']['humanTimestamp']
        ini['test_webserver'] = confyml['misc']['test_webserver']
        ini['Mailing'] = confyml['debug']['Mailing']
        ini['MyName'] = socket.gethostname()
        ini['My_IP'] = self.get_external_ip()
        system = platform.system()
        ini['System'] = system
        ini['ProgramName'] = self.progname
        ini['Tasks'] = confyml['DeSeTask'][system]
        ini['TargetNet'] = confyml['Communication']['TargetNet']
        
        logging.basicConfig(
            level=getattr(logging, confyml['misc']["loglevel"].upper(), logging.INFO), # INFO is default  
            #level=logging.DEBUG, 
            format='%(asctime)s :: %(levelname)-7s :: [%(name)+16s] [%(lineno)+3s] :: %(message)s',
            datefmt=ini['debugdatefmt'],
            handlers=[
                logging.FileHandler(f"{ini['LogPath']}/{self.progname[:-3]}_{socket.gethostname()+ini['StartTime'].strftime(ini['logSuffix'])}.log"),
                logging.StreamHandler()
            ])

        logger.info("")
        logger.info(f"---------- starting {self.progname} at {ini['StartTime']} ----------")

        tm = ThreadManager()  
        ini['ThreadManager'] = tm     

        #ini['ThreadManager'].start("CPU", target=system_monitor_thread._cpu_monitor)
        #ini['ThreadManager'].start("ETH", target=system_monitor_thread._eth_monitor)
        #ini['ThreadManager'].start("sdx", target=system_monitor_thread._sdx_monitor)
        #ini['ThreadManager'].start("system", target=system_monitor_thread._system_monitor)
        #ini['ThreadManager'].start("weather", target=weather_thread.run)
        #ini['ThreadManager'].start("SystemMonitor", target=system_monitor_thread._system_monitor)
        logger.info(f"Initialisation complete")
