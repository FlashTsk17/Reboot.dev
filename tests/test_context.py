from services.context import build_context
from services.ingestion.models import RepositoryFile, RepositorySnapshot
from services.analysis.ast import analyze_source
from services.analysis.graph import build_graph

def test_context_merges_analysis_layers():
    snapshot = RepositorySnapshot("FlashTsk17", "Demo", "FlashTsk17/Demo", "main", "main", "abc", [
        RepositoryFile("src/main.ts", 30, "a"), RepositoryFile("src/helper.ts", 20, "b"), RepositoryFile("README.md", 10, "c")
    ])
    texts = {"src/main.ts": 'import { helper } from "./helper"; fetch("/api");'}
    asts = [analyze_source(path, text) for path, text in texts.items()]
    graph = build_graph(asts, [f.path for f in snapshot.files])
    ctx = build_context(snapshot, texts, asts, graph)
    data = ctx.to_dict()
    assert data["schema_version"] == "reboot-project-context/v0.1"
    assert data["statistics"]["total_files"] == 3
    assert data["statistics"]["graph_edges"] >= 1
    assert "NETWORK_CALL" in data["signals"]
    assert "src/main.ts" in data["entry_points"]

def test_context_preserves_unresolved_dependencies():
    snapshot = RepositorySnapshot("a", "b", "a/b", "main", "main", "abc", [RepositoryFile("src/a.ts")])
    text = 'import x from "./missing";'
    ast = analyze_source("src/a.ts", text)
    graph = build_graph([ast], ["src/a.ts"])
    ctx = build_context(snapshot, {"src/a.ts": text}, [ast], graph)
    assert ctx.unresolved_dependencies
