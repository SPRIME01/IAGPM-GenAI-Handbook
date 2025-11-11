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
    def load(self) -> dict:
        if not self._path.exists():
            return {}
        try:
            raw = self._path.read_text(encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(f"Unable to read configuration file {self._path}") from exc

        if self._path.suffix in {".yml", ".yaml"}:
            try:
                return yaml.safe_load(raw) or {}
            except yaml.YAMLError as exc:
                raise ValueError(f"Invalid YAML in {self._path}") from exc

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {self._path}") from exc
