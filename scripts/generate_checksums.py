from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INCLUDED = ("openapi", "schemas", "docs", "generated", "fixtures")


def files() -> list[Path]:
    paths = [ROOT / "VERSION"]
    for directory in INCLUDED:
        paths.extend(path for path in (ROOT / directory).rglob("*") if path.is_file())
    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def main() -> None:
    for path in files():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{digest}  {path.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
