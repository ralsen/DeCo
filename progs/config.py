#!/usr/bin/env python3 xxx
# -*- coding: utf-8 -*-
import logging
import yaml
import os

logger = logging.getLogger(__name__)


def init(ProgName):
    global ini

    ini = {}
    current_dir = os.getcwd()
    print(f"---> {current_dir}")
    current_dir += '/..'
    with open(f'{current_dir}/yml/config.yml', 'r') as ymlfile:
        ini['yml'] = yaml.safe_load(ymlfile)

    RootPath = current_dir #yml['ROOT_PATH']
    ini['LogPath'] = RootPath + ini['yml']['pathes']['LOG']
    ini['DataPath'] = RootPath + ini['yml']['pathes']['DATA']
    ini['RRDPath'] = RootPath + ini['yml']['pathes']['RRD']
    ini['YMLPath'] = RootPath + ini['yml']['pathes']['YML']
    ini['PNGPath'] = RootPath + ini['yml']['pathes']['PNG']
    ini['DaboServerName'] = ini['yml']['Communication']['DaboServerName']
    ini['DaboServerPort'] = ini['yml']['Communication']['DaboServerPort']
    ini['debugdatefmt'] = ini['yml']['debug']['datefmt']
    ini['logSuffix'] = ini['yml']['suffixes']['log']
    ini['dataSuffix'] = ini['yml']['suffixes']['data']
    ini['hirestime'] = ini['yml']['debug']['hirestime']
    ini['humanTimestamp'] = ini['yml']['debug']['humanTimestamp']
    ini['Mailing'] = ini['yml']['debug']['Mailing']

