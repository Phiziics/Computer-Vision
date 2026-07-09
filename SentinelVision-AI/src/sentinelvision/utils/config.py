from pathlib import Path
from typing import Any

import yaml


def load_config(config_path: str | Path) -> dict[str, Any]:
    """
    Load a YAML configuration file.

    Parameters
    ----------
    config_path:
        Path to the YAML configuration file.

    Returns
    -------
    dict[str, Any]
        Parsed configuration values.
    """
    path = Path(config_path)

    # Fail early when the configuration file does not exist.
    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        )

    # Read YAML safely.
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # Protect against empty YAML files.
    if config is None:
        return {}

    return config