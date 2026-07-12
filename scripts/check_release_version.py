from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    tag = sys.argv[1] if len(sys.argv) > 1 else None
    artifact = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    openapi = yaml.safe_load((ROOT / "openapi" / "openapi.yaml").read_text(encoding="utf-8"))
    values = {
        "VERSION": version,
        "OpenAPI info.version": str(openapi["info"]["version"]),
        "pyproject project.version": str(pyproject["project"]["version"]),
        "package.json version": str(package["version"]),
    }
    mismatches = {name: value for name, value in values.items() if value != version}
    if mismatches:
        raise SystemExit(f"Version mismatch against VERSION={version}: {mismatches}")
    if tag is not None:
        if not tag.startswith("v"):
            raise SystemExit(f"Release tag must start with v: {tag}")
        tag_version = tag[1:]
        if tag_version != version:
            raise SystemExit(f"Tag version {tag_version} does not match VERSION {version}")
    if artifact is not None:
        expected_name = f"automation-platform-contracts-v{version}.zip"
        if artifact.name != expected_name or not artifact.is_file():
            raise SystemExit(f"Release artifact must be {expected_name}: {artifact}")
    print(f"PASS: release version {version} is consistent")


if __name__ == "__main__":
    main()
