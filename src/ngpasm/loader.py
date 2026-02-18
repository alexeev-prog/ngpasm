# loader.py
"""
Loader module for NGPASM.

This module provides functionality for reading configuration files
with support for multiple formats and proper error handling.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Any

import orjson as json
import toml
import yaml


class ConfigType(Enum):
    """Project configuration types."""

    TOML = auto()
    YAML = auto()
    JSON = auto()


@dataclass(frozen=True)
class ConfigTypeDetector:
    """Strategy for detecting configuration file types."""

    @staticmethod
    def by_extension(extension: str) -> ConfigType:
        """
        Detect config type by file extension.

        Args:
            extension: File extension string

        Returns:
            Detected config type (defaults to JSON)

        """
        cleaned: str = extension.lower().lstrip(".")

        detectors: dict[str, ConfigType] = {
            "json": ConfigType.JSON,
            "yaml": ConfigType.YAML,
            "yml": ConfigType.YAML,
            "toml": ConfigType.TOML,
        }

        return detectors.get(cleaned, ConfigType.JSON)

    @staticmethod
    def by_filename(filename: str) -> ConfigType:
        """
        Detect config type by filename.

        Args:
            filename: Full filename or path

        Returns:
            Detected config type

        """
        extension: str = Path(filename).suffix.lstrip(".") or filename
        return ConfigTypeDetector.by_extension(extension)


class ConfigLoader(ABC):
    """Abstract base class for configuration loaders."""

    @abstractmethod
    def load(self, filepath: Path) -> dict[str, Any]:
        """Load configuration from file."""


class JsonConfigLoader(ConfigLoader):
    """JSON configuration loader."""

    def load(self, filepath: Path) -> dict[str, Any]:
        with filepath.open("rb") as f:
            return json.loads(f.read())


class YamlConfigLoader(ConfigLoader):
    """YAML configuration loader."""

    def load(self, filepath: Path) -> dict[str, Any]:
        with filepath.open() as f:
            return yaml.safe_load(f)


class TomlConfigLoader(ConfigLoader):
    """TOML configuration loader."""

    def load(self, filepath: Path) -> dict[str, Any]:
        with filepath.open() as f:
            return toml.load(f)


class ConfigReader:
    """
    Project configuration reader with strategy pattern.

    This class uses different loaders based on configuration type
    and provides consistent error handling.
    """

    _loaders: dict[
        ConfigType, JsonConfigLoader | TomlConfigLoader | YamlConfigLoader
    ] = {
        ConfigType.JSON: JsonConfigLoader(),
        ConfigType.YAML: YamlConfigLoader(),
        ConfigType.TOML: TomlConfigLoader(),
    }

    def __init__(self, config_file: str, configtype: ConfigType | None = None) -> None:
        """
        Initialize configuration reader.

        Args:
            config_file: Path to configuration file
            configtype: Explicit config type (auto-detected if None)

        Raises:
            FileNotFoundError: If config file doesn't exist
            TypeError: If loaded data is not a dictionary

        """
        self.config_file = Path(config_file)
        self.configtype = configtype or ConfigTypeDetector.by_filename(config_file)
        self.config = self._load_data()

    def _load_data(self) -> dict[str, Any]:
        """
        Load configuration data using appropriate loader.

        Returns:
            Loaded data as dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            TypeError: If loaded data is not a dictionary

        """
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")

        loader: JsonConfigLoader | TomlConfigLoader | YamlConfigLoader | None = (
            self._loaders.get(self.configtype)
        )
        if not loader:
            raise ValueError(f"Unsupported configuration type: {self.configtype}")

        data: dict[str, Any] = loader.load(self.config_file)

        if not isinstance(data, dict):
            raise TypeError(
                f"Invalid data in {self.config_file}: expected dict, got {type(data).__name__}"
            )

        return data
