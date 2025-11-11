from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from policy_gateway.ports.configuration import ConfigurationPort


class ConfigFileAdapter(ConfigurationPort):
    """Adapter that loads configuration data from a JSON or YAML file."""

    def __init__(self, path: str | os.PathLike[str]):
        self._path = Path(path)

    def load(self) -> dict:
        if not self._path.exists():
            return {}
        try:
            if self._path.suffix in {".yml", ".yaml"}:
                return yaml.safe_load(self._path.read_text()) or {}
            return json.loads(self._path.read_text())
        except Exception as e:
            import logging
            logging.error(f"Failed to load configuration from {self._path}: {e}")
            return {}
