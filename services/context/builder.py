from pathlib import PurePosixPath
from typing import Any
from services.analysis.classifier import classify
from services.analysis.ast.models import CodeFileAST
from services.analysis.graph.models import DependencyGraph
from services.ingestion.models import RepositorySnapshot
from .models import ProjectContext

ENTRY_NAMES = {"main.ts", "main.tsx", "main.js", "main.jsx", "server.ts", "server.js", "index.ts", "index.tsx", "index.js"}


def build_context(snapshot: RepositorySnapshot, source_text: dict[str, str], asts: list[CodeFileAST], graph: DependencyGraph) -> ProjectContext:
    ast_by_path = {a.path: a for a in asts}
    files: list[dict[str, Any]] = []
    signals: list[str] = []
    entry_points: list[str] = []
    important: list[str] = []
    layer_counts: dict[str, int] = {}

    for f in snapshot.files:
        c = classify(f.path, f.size)
        item = {
            "path": f.path,
            "size": f.size,
            "sha": f.sha,
            "category": c.category,
            "language": c.language,
            "layer": c.layer,
            "importance": c.importance,
            "reasons": list(c.reasons),
        }
        files.append(item)
        layer_counts[c.layer] = layer_counts.get(c.layer, 0) + 1
        if PurePosixPath(f.path).name in ENTRY_NAMES:
            entry_points.append(f.path)
        if c.importance in {"CRITICAL", "HIGH"}:
            important.append(f.path)
        ast = ast_by_path.get(f.path)
        if ast:
            signals.extend(ast.signals)
            if ast.symbols and c.importance in {"CRITICAL", "HIGH", "MEDIUM"}:
                important.append(f.path)

    dependencies = [{"source": e.source, "target": e.target, "type": e.type, "file": e.file, "line": e.line} for e in graph.edges]
    unresolved = [{"source": e.source, "target": e.target, "type": e.type, "file": e.file, "line": e.line} for e in graph.unresolved]
    modules = sorted({str(PurePosixPath(f["path"]).parent) for f in files if f["category"] == "SOURCE"})

    stats = {
        "total_files": len(files),
        "source_files": sum(f["category"] == "SOURCE" for f in files),
        "test_files": sum(f["category"] == "TEST" for f in files),
        "config_files": sum(f["category"] == "CONFIG" for f in files),
        "documentation_files": sum(f["category"] == "DOCUMENTATION" for f in files),
        "graph_nodes": len(graph.nodes),
        "graph_edges": len(graph.edges),
        "unresolved_dependencies": len(graph.unresolved),
        "source_text_files": len(source_text),
        "source_text_coverage": "partial" if len(source_text) < stats_source(files) else "complete",
    }
    return ProjectContext(
        schema_version="reboot-project-context/v0.1",
        repository={"owner": snapshot.owner, "name": snapshot.name, "full_name": snapshot.full_name, "default_branch": snapshot.default_branch},
        revision={"ref": snapshot.ref, "commit_sha": snapshot.commit_sha},
        files=files,
        architecture={"layers": layer_counts, "modules": modules},
        entry_points=sorted(set(entry_points)),
        important_components=sorted(set(important)),
        dependencies=dependencies,
        unresolved_dependencies=unresolved,
        signals=signals,
        statistics=stats,
    )


def stats_source(files: list[dict[str, Any]]) -> int:
    return sum(f["category"] == "SOURCE" for f in files)
