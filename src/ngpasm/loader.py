"""
Loader module for NGPASM.

This module have a functional for reading config files.
"""
from enum import Enum
from pathlib import Path

import orjson as json
import toml
import yaml


class ConfigType(Enum):
    """Project configuration types."""

    TOML = 0
    YAML = 1
    JSON = 2


def detect_config_type_by_extension(extension: str) -> ConfigType:
    """
    Detect config type by file extension.

    Args:
        extension: File extension string

    Returns:
        ConfigType: Detected config type (defaults to JSON)

    """
    cleaned_extension = extension.lower().lstrip(".")

    if cleaned_extension == "json":
        return ConfigType.JSON
    if cleaned_extension in ("yaml", "yml"):
        return ConfigType.YAML
    if cleaned_extension == "toml":
        return ConfigType.TOML
    return ConfigType.JSON


def detect_config_type_by_filename(filename: str) -> ConfigType:
    """
    Detect config type by filename.

    Args:
        filename: Full filename or path

    Returns:
        ConfigType: Detected config type

    """
    extension = Path(filename).suffix.lstrip(".") or filename
    return detect_config_type_by_extension(extension)


class ConfigReader:
    """Project configuration reader."""

    def __init__(self, config_file: str, configtype: ConfigType = None):
        """
        Constructs new instance.

        Args:
            config_file: Path to configuration file
            configtype: Explicit config type (auto-detected if None)

        """
        self.config_file = Path(config_file)

        if configtype is None:
            self.configtype = detect_config_type_by_filename(config_file)
        else:
            self.configtype = configtype

        self.config = self._load_data_from_config()

    def _load_data_from_config(self) -> dict:
        """
        Load configuration data from file.

        Returns:
            dict: loaded data as dictionary

        """
        data = {}

        if not self.config_file.exists():
            return data

        if self.configtype == ConfigType.YAML:
            with self.config_file.open() as f:
                data = yaml.safe_load(f)
        elif self.configtype == ConfigType.TOML:
            with self.config_file.open() as f:
                data = toml.load(f)
        elif self.configtype == ConfigType.JSON:
            with self.config_file.open("rb") as f:
                data = json.loads(f.read())

        return data if isinstance(data, dict) else {}
