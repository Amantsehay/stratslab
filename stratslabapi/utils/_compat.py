import tomllib
from importlib.metadata import metadata as _metadata
from typing import Any

__anll__ = [
    "config",
    "metadata",
]

def _get_config() -> dict[str, Any]:
    with open("pyproject.toml", "rb") as f:
        return tomllib.load(f)


metadata = _metadata("stratslabapi")
config: dict[str, Any] = _get_config()
