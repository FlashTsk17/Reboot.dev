from dataclasses import dataclass, field
from typing import Literal

FileKind = Literal["SOURCE", "TEST", "CONFIG", "DOCUMENTATION", "ASSET", "DEPENDENCY", "GENERATED", "UNKNOWN"]

@dataclass(frozen=True)
class RepositoryFile:
    path: str
    size: int = 0
    sha: str | None = None
    kind: FileKind = "UNKNOWN"

@dataclass(frozen=True)
class RepositorySnapshot:
    owner: str
    name: str
    full_name: str
    default_branch: str
    ref: str
    commit_sha: str
    files: list[RepositoryFile] = field(default_factory=list)

    @property
    def stats(self) -> dict[str, int]:
        return {
            "total_files": len(self.files),
            "source_files": sum(f.kind == "SOURCE" for f in self.files),
            "test_files": sum(f.kind == "TEST" for f in self.files),
            "config_files": sum(f.kind == "CONFIG" for f in self.files),
            "documentation_files": sum(f.kind == "DOCUMENTATION" for f in self.files),
        }
