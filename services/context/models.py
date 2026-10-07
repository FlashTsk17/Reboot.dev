from dataclasses import dataclass, field
from typing import Any

@dataclass
class ProjectContext:
    schema_version: str
    repository: dict[str, Any]
    revision: dict[str, str]
    files: list[dict[str, Any]] = field(default_factory=list)
    architecture: dict[str, Any] = field(default_factory=dict)
    entry_points: list[str] = field(default_factory=list)
    important_components: list[str] = field(default_factory=list)
    dependencies: list[dict[str, Any]] = field(default_factory=list)
    unresolved_dependencies: list[dict[str, Any]] = field(default_factory=list)
    signals: list[str] = field(default_factory=list)
    statistics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "repository": self.repository,
            "revision": self.revision,
            "files": self.files,
            "architecture": self.architecture,
            "entry_points": self.entry_points,
            "important_components": self.important_components,
            "dependencies": self.dependencies,
            "unresolved_dependencies": self.unresolved_dependencies,
            "signals": sorted(set(self.signals)),
            "statistics": self.statistics,
        }
