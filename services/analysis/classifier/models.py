from dataclasses import dataclass
from typing import Literal

Language = Literal["TypeScript", "TSX", "JavaScript", "JSX", "Python", "JSON", "Markdown", "CSS", "Unknown"]
Layer = Literal["FRONTEND", "BACKEND", "API", "DATABASE", "TEST", "CONFIG", "DOCUMENTATION", "UNKNOWN"]
Importance = Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "IGNORE"]

@dataclass(frozen=True)
class Classification:
    path: str
    category: str
    language: Language
    layer: Layer
    importance: Importance
    reasons: tuple[str, ...]
