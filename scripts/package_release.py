from __future__ import annotations

import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
INCLUDED = ("openapi", "schemas", "docs", "generated", "fixtures")


def release_files() -> list[Path]:
    paths = [ROOT / "VERSION"]
    for directory in INCLUDED:
        paths.extend(path for path in (ROOT / directory).rglob("*") if path.is_file())
    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def main() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_contracts.py"], cwd=ROOT, text=True, capture_output=True
    )
    if result.returncode:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit("Refusing to package a failing contract baseline")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        raise SystemExit("VERSION must not be empty")
    DIST.mkdir(exist_ok=True)
    report = DIST / "VALIDATION_REPORT.txt"
    report.write_text(result.stdout, encoding="utf-8", newline="\n")
    checksums = DIST / "SHA256SUMS.txt"
    lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT).as_posix()}"
        for path in release_files()
    ]
    checksums.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    artifact = DIST / f"automation-platform-contracts-v{version}.zip"
    with zipfile.ZipFile(artifact, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in release_files():
            archive.write(path, path.relative_to(ROOT).as_posix())
        archive.write(checksums, checksums.name)
        archive.write(report, report.name)
    print(f"PASS: release package created at {artifact.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
