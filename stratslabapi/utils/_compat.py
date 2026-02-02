import tomllib
from importlib.metadata import metadata as _metadata
from pathlib import Path
from typing import Any

__anll__ = [
    "config",
    "metadata",
]

def _get_config() -> dict[str, Any]:
    # Find pyproject.toml by traversing up from the current file
    current_dir = Path(__file__).parent
    while current_dir != current_dir.parent:
        pyproject_path = current_dir / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                return tomllib.load(f)
        current_dir = current_dir.parent

    # Fallback to trying relative path
    with open("pyproject.toml", "rb") as f:
        return tomllib.load(f)


def _get_metadata():
    try:
        return _metadata("stratslabapi")
    except Exception:
        # Fallback: return a minimal metadata dict if the package metadata cannot be found
        config = _get_config()
        tool_poetry = config.get("tool", {}).get("poetry", {})
        return {
            "version": tool_poetry.get("version", "0.1.0"),
            "name": tool_poetry.get("name", "stratslab"),
        }


metadata = _get_metadata()
config: dict[str, Any] = _get_config()
