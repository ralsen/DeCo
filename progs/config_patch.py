#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import platform
import socket
from pathlib import Path
from typing import Any

import yaml

from threadmanager import ThreadManager

logger = logging.getLogger(__name__)


class InitManager:
    def __init__(self, progname: str):
        self.ini: dict[str, Any] = {}
        self.progname = progname
        self.load_init()

    def get_external_ip(self) -> str | None:
        try:
            # UDP "connect" does not send packets but resolves the outbound interface.
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except OSError as exc:
            logger.warning("Could not determine external IP: %s", exc)
            return None

    @staticmethod
    def _safe_get(mapping: dict, path: list[str], default: Any = None) -> Any:
        cur: Any = mapping
        for key in path:
            if not isinstance(cur, dict) or key not in cur:
                return default
            cur = cur[key]
        return cur

    @staticmethod
    def _resolve_under_root(root: Path, raw_path: str) -> Path:
        """
        Keep configured paths inside root. Reject absolute or traversal paths.
        """
        candidate = Path(raw_path)
        if candidate.is_absolute():
            raise ValueError(f"Absolute path not allowed in config: {raw_path}")

        resolved = (root / candidate).resolve()
        if resolved != root and root not in resolved.parents:
            raise ValueError(f"Path escapes project root: {raw_path}")
        return resolved

    def _load_yaml_config(self, config_path: Path) -> dict:
        try:
            with config_path.open("r", encoding="utf-8") as ymlfile:
                data = yaml.safe_load(ymlfile)
        except FileNotFoundError as exc:
            raise RuntimeError(f"Config file not found: {config_path}") from exc
        except yaml.YAMLError as exc:
            raise RuntimeError(f"Invalid YAML in config file: {config_path}") from exc
        except OSError as exc:
            raise RuntimeError(f"Could not read config file: {config_path}") from exc

        if not isinstance(data, dict):
            raise RuntimeError(f"Config root must be a mapping: {config_path}")
        return data

    def _setup_logging(self, ini: dict[str, Any], confyml: dict[str, Any]) -> None:
        loglevel_name = str(self._safe_get(confyml, ["misc", "loglevel"], "INFO")).upper()
        loglevel = getattr(logging, loglevel_name, logging.INFO)
        datefmt = str(self._safe_get(confyml, ["debug", "datefmt"], "%Y-%m-%d %H:%M:%S"))

        logfile = ini["LogPath"] / (
            f"{self.progname[:-3]}_"
            f"{socket.gethostname() + ini['StartTime'].strftime(ini['logSuffix'])}.log"
        )

        handlers: list[logging.Handler] = [logging.StreamHandler()]
        try:
            ini["LogPath"].mkdir(parents=True, exist_ok=True)
            handlers.insert(0, logging.FileHandler(logfile, encoding="utf-8"))
        except OSError as exc:
            logger.warning("Could not create file logger at %s: %s", logfile, exc)

        logging.basicConfig(
            level=loglevel,
            format="%(asctime)s :: %(levelname)-7s :: [%(name)+16s] [%(lineno)+3s] :: %(message)s",
            datefmt=datefmt,
            handlers=handlers,
            force=True,
        )

    def load_init(self) -> None:
        file_dir = Path(__file__).resolve().parent
        root_path = file_dir.parent.resolve()
        config_path = root_path / "yml" / "config.yml"
        confyml = self._load_yaml_config(config_path)

        ini = self.ini
        ini["StartTime"] = datetime.datetime.now()
        ini["confyml"] = confyml

        pathes = self._safe_get(confyml, ["pathes"], {})
        if not isinstance(pathes, dict):
            raise RuntimeError("Config key 'pathes' must be a mapping.")

        required_path_keys = {
            "LOG": "LogPath",
            "DATA": "DataPath",
            "RRD": "RRDPath",
            "YML": "YMLPath",
            "PNG": "PNGPath",
            "REG": "REGPath",
        }
        for cfg_key, ini_key in required_path_keys.items():
            raw = pathes.get(cfg_key)
            if not isinstance(raw, str) or not raw.strip():
                raise RuntimeError(f"Missing/invalid pathes.{cfg_key} in config.")
            ini[ini_key] = self._resolve_under_root(root_path, raw)

        ini["DeSePort"] = self._safe_get(confyml, ["Communication", "DevServerPort"])
        ini["DeSeName"] = self._safe_get(confyml, ["Communication", "DevServerName"])
        ini["debugdatefmt"] = self._safe_get(confyml, ["debug", "datefmt"], "%Y-%m-%d %H:%M:%S")
        ini["logSuffix"] = self._safe_get(confyml, ["suffixes", "log"], "_%Y%m%d_%H%M%S.log")
        ini["dataSuffix"] = self._safe_get(confyml, ["suffixes", "data"], "_%Y%m%d")
        ini["hirestime"] = self._safe_get(confyml, ["debug", "hirestime"], False)
        ini["SystemMonitorSleep"] = self._safe_get(confyml, ["Timers", "SystemMonitorSleep"], 5)
        ini["mainloop_sleep"] = self._safe_get(confyml, ["Timers", "mainloop_sleep"], 1)
        ini["humanTimestamp"] = self._safe_get(confyml, ["misc", "humanTimestamp"], True)
        ini["test_webserver"] = self._safe_get(confyml, ["misc", "test_webserver"], False)
        ini["Mailing"] = self._safe_get(confyml, ["debug", "Mailing"], False)
        ini["MyName"] = socket.gethostname()
        ini["My_IP"] = self.get_external_ip()
        ini["System"] = platform.system()
        ini["ProgramName"] = self.progname

        tasks_by_system = self._safe_get(confyml, ["DeSeTask"], {})
        if not isinstance(tasks_by_system, dict):
            raise RuntimeError("Config key 'DeSeTask' must be a mapping.")
        ini["Tasks"] = tasks_by_system.get(ini["System"], [])
        ini["TargetNet"] = self._safe_get(confyml, ["Communication", "TargetNet"], "")

        self._setup_logging(ini, confyml)
        logger.info("")
        logger.info("---------- starting %s at %s ----------", self.progname, ini["StartTime"])

        ini["ThreadManager"] = ThreadManager()
        logger.info("Initialisation complete")

