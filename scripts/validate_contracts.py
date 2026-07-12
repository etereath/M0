from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from generate_reference_types import collect_enum_specs, render_manifest, render_python, render_typescript


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
FORMAT_CHECKER = FormatChecker()
TEXT_SUFFIXES = {".json", ".yaml", ".yml", ".md", ".py", ".ts", ".csv", ".toml", ".txt"}
SECRET_PATTERNS = (
    re.compile(rb"gh[pousr]_[A-Za-z0-9_]+"),
    re.compile(rb"github_pat_[A-Za-z0-9_]+"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
    re.compile(rb"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
)
ABSOLUTE_PATH_PATTERN = re.compile(rb"(?:[A-Za-z]:\\\\|/(?:Users|home)/)")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def walk(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def json_pointer(document: object, fragment: str, source: str) -> object:
    if not fragment or fragment == "#":
        return document
    if not fragment.startswith("#/"):
        raise AssertionError(f"Unsupported JSON Pointer in {source}: {fragment}")
    current = document
    for token in fragment[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        try:
            current = current[int(token)] if isinstance(current, list) else current[token]
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            raise AssertionError(f"Missing JSON Pointer target in {source}: {fragment}") from exc
    return current


def load_schemas() -> tuple[dict[str, dict], Registry]:
    schemas: dict[str, dict] = {}
    registry = Registry()
    for path in sorted(SCHEMA_DIR.rglob("*.schema.json")):
        schema = read_json(path)
        if not isinstance(schema, dict) or not isinstance(schema.get("$id"), str):
            raise AssertionError(f"Schema needs a string $id: {path.relative_to(ROOT)}")
        if path.name in schemas:
            raise AssertionError(f"Duplicate schema filename: {path.name}")
        Draft202012Validator.check_schema(schema)
        schemas[path.name] = schema
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return schemas, registry


def validate_serialization_files() -> None:
    for path in sorted(ROOT.rglob("*.json")):
        read_json(path)
    for path in sorted(list(ROOT.rglob("*.yaml")) + list(ROOT.rglob("*.yml"))):
        yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_fixtures(schemas: dict[str, dict], registry: Registry) -> tuple[int, int]:
    def validator(schema_name: str) -> Draft202012Validator:
        try:
            return Draft202012Validator(
                schemas[schema_name], registry=registry, format_checker=FORMAT_CHECKER
            )
        except KeyError as exc:
            raise AssertionError(f"Fixture references unknown schema: {schema_name}") from exc

    valid_count = 0
    for path in sorted((ROOT / "fixtures" / "valid").glob("*.json")):
        stem = path.name.removesuffix(".valid.json")
        schema_name = f"{stem}.schema.json"
        payload = read_json(path)
        errors = sorted(validator(schema_name).iter_errors(payload), key=lambda error: list(error.path))
        if errors:
            raise AssertionError(f"Valid fixture failed: {path.name}: {errors[0].message}")
        valid_count += 1

    invalid_count = 0
    for path in sorted((ROOT / "fixtures" / "invalid").glob("*.json")):
        wrapper = read_json(path)
        if not isinstance(wrapper, dict) or not isinstance(wrapper.get("_expected_schema"), str):
            raise AssertionError(f"Invalid fixture needs _expected_schema: {path.name}")
        if "_payload" not in wrapper:
            raise AssertionError(f"Invalid fixture needs _payload: {path.name}")
        errors = list(validator(wrapper["_expected_schema"]).iter_errors(wrapper["_payload"]))
        if not errors:
            raise AssertionError(f"Invalid fixture unexpectedly passed: {path.name}")
        invalid_count += 1
    return valid_count, invalid_count


def validate_openapi_refs() -> None:
    path = ROOT / "openapi" / "openapi.yaml"
    spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict) or not str(spec.get("openapi", "")).startswith("3.1."):
        raise AssertionError("OpenAPI document must declare OpenAPI 3.1")
    if not spec.get("info", {}).get("version") or not spec.get("paths"):
        raise AssertionError("OpenAPI document must include info.version and paths")
    for node in walk(spec):
        reference = node.get("$ref") if isinstance(node, dict) else None
        if not isinstance(reference, str):
            continue
        if reference.startswith("#"):
            json_pointer(spec, reference, "openapi/openapi.yaml")
            continue
        parsed = urlparse(reference)
        if parsed.scheme or reference.startswith("//"):
            continue
        file_part, _, fragment = reference.partition("#")
        target = (path.parent / unquote(file_part)).resolve()
        if not target.is_file() or ROOT.resolve() not in target.parents:
            raise AssertionError(f"Missing or unsafe OpenAPI ref: {reference}")
        if target.suffix == ".json":
            json_pointer(read_json(target), f"#{fragment}" if fragment else "#", reference)
        elif target.suffix in {".yaml", ".yml"}:
            json_pointer(yaml.safe_load(target.read_text(encoding="utf-8")), f"#{fragment}" if fragment else "#", reference)
        else:
            raise AssertionError(f"Unsupported OpenAPI ref target: {reference}")


def validate_text_files() -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        data = path.read_bytes()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AssertionError(f"Non-UTF-8 text file: {path.relative_to(ROOT)}") from exc
        if any(pattern.search(data) for pattern in SECRET_PATTERNS):
            raise AssertionError(f"Potential credential found: {path.relative_to(ROOT)}")
        if ABSOLUTE_PATH_PATTERN.search(data):
            raise AssertionError(f"Absolute local path found: {path.relative_to(ROOT)}")


def validate_generated_references(schemas: dict[str, dict]) -> None:
    for schema in schemas.values():
        for node in walk(schema):
            enum = node.get("enum") if isinstance(node, dict) else None
            if isinstance(enum, list):
                frozen = tuple(json.dumps(item, sort_keys=True, ensure_ascii=False) for item in enum)
                if len(frozen) != len(set(frozen)):
                    raise AssertionError(f"Duplicate enum value: {enum}")
    specs = collect_enum_specs(SCHEMA_DIR)
    expected = {
        ROOT / "generated" / "python" / "enums.py": render_python(specs),
        ROOT / "generated" / "typescript" / "enums.ts": render_typescript(specs),
        ROOT / "generated" / "enum-manifest.json": render_manifest(specs),
    }
    for path, content in expected.items():
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            raise AssertionError(f"Generated reference is out of sync with schemas: {path.relative_to(ROOT)}")


def validate_python_syntax() -> None:
    for path in sorted(ROOT.rglob("*.py")):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def main() -> None:
    schemas, registry = load_schemas()
    validate_serialization_files()
    valid_count, invalid_count = validate_fixtures(schemas, registry)
    validate_openapi_refs()
    validate_text_files()
    validate_generated_references(schemas)
    validate_python_syntax()
    print(
        "PASS: "
        f"{len(schemas)} schemas, {valid_count} valid fixtures, "
        f"{invalid_count} invalid fixtures, OpenAPI refs OK, UTF-8 OK"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
