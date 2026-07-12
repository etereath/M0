from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


@dataclass(frozen=True)
class EnumSpec:
    name: str
    source: str
    pointer: str
    values: tuple[str, ...]


NAME_OVERRIDES = {
    "common": {
        "actor_type": "ActorType",
        "evidence_type": "EvidenceType",
        "risk_level": "RiskLevel",
        "source_type": "SourceType",
    },
    "employee": {"role": "EmployeeRole"},
    "task": {"task_mode": "TaskMode", "status": "TaskStatus"},
    "assignment": {"status": "AssignmentStatus", "assignment_method": "AssignmentMethod"},
    "task_update": {"update_type": "TaskUpdateType"},
    "task_command": {"command_type": "TaskCommandType"},
    "project": {"status": "ProjectStatus", "priority": "ProjectPriority"},
    "project_update": {"update_type": "ProjectUpdateType", "suggested_status": "ProjectUpdateSuggestedStatus"},
    "inventory_transaction": {"transaction_type": "InventoryTransactionType"},
    "agent_proposal": {"proposal_type": "AgentProposalType"},
    "approval": {"approval_type": "ApprovalType", "status": "ApprovalStatus"},
    "sync_event": {
        "direction": "SyncDirection",
        "entity_type": "SyncEntityType",
        "operation": "SyncOperation",
        "status": "SyncStatus",
    },
    "audit_event": {"result": "AuditResult"},
}


def walk(value: object, pointer: str = ""):
    if isinstance(value, dict):
        yield pointer, value
        for key, child in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            yield from walk(child, f"{pointer}/{escaped}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{pointer}/{index}")


def collect_enum_specs(schema_dir: Path = SCHEMA_DIR) -> list[EnumSpec]:
    specs: list[EnumSpec] = []
    existing: dict[str, EnumSpec] = {}
    for path in sorted(schema_dir.rglob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        stem = path.name.removesuffix(".schema.json")
        for pointer, node in walk(schema):
            if "/if/" in pointer or "/then/" in pointer or "/else/" in pointer:
                continue
            enum = node.get("enum") if isinstance(node, dict) else None
            if not isinstance(enum, list):
                continue
            values = tuple(item for item in enum if isinstance(item, str))
            if not values:
                continue
            property_name = pointer.rsplit("/", 1)[-1]
            name = NAME_OVERRIDES.get(stem, {}).get(property_name)
            if name is None:
                name = "".join(part.capitalize() for part in re.split(r"[^A-Za-z0-9]+", property_name))
                name = f"{stem.title().replace('_', '')}{name}"
            if name in existing:
                if existing[name].values == values:
                    continue
                raise ValueError(f"Duplicate generated enum name with different values: {name}")
            spec = EnumSpec(name, path.relative_to(ROOT).as_posix(), pointer, values)
            existing[name] = spec
            specs.append(spec)
    return specs


def render_python(specs: list[EnumSpec]) -> str:
    lines = ["# Generated from schemas; do not edit manually.\n", "from enum import StrEnum\n\n"]
    for spec in specs:
        lines.append(f"class {spec.name}(StrEnum):\n")
        for value in spec.values:
            lines.append(f"    {value} = \"{value}\"\n")
        lines.append("\n")
    return "".join(lines).rstrip() + "\n"


def render_typescript(specs: list[EnumSpec]) -> str:
    lines = ["// Generated from schemas; do not edit manually.\n"]
    for spec in specs:
        lines.append(f"export const {spec.name} = [\n")
        for value in spec.values:
            lines.append(f'  "{value}",\n')
        lines.append("] as const;\n")
        lines.append(f"export type {spec.name} = typeof {spec.name}[number];\n\n")
    return "".join(lines).rstrip() + "\n"


def render_manifest(specs: list[EnumSpec]) -> str:
    data = [
        {"name": spec.name, "source": spec.source, "pointer": spec.pointer, "values": list(spec.values)}
        for spec in specs
    ]
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    specs = collect_enum_specs()
    (ROOT / "generated" / "python" / "enums.py").write_text(render_python(specs), encoding="utf-8", newline="\n")
    (ROOT / "generated" / "typescript" / "enums.ts").write_text(render_typescript(specs), encoding="utf-8", newline="\n")
    (ROOT / "generated" / "enum-manifest.json").write_text(render_manifest(specs), encoding="utf-8", newline="\n")
    print(f"Generated {len(specs)} enum types")


if __name__ == "__main__":
    main()
