from services.analysis.ast import analyze_source
from services.analysis.graph import build_graph

def test_ast_extracts_imports_symbols_calls_and_signals():
    source = 'import { scoreAnswers } from "./scoring";\\nexport function run() { fetch("/api"); scoreAnswers([]); }'
    ast = analyze_source("backend/src/server.ts", source)
    assert ast.imports[0].source == "./scoring"
    assert "run" in ast.exports
    assert any(s.name == "run" for s in ast.symbols)
    assert "NETWORK_CALL" in ast.signals

def test_graph_resolves_local_imports_and_tracks_unresolved():
    a = analyze_source("src/a.ts", 'import { b } from "./b"; import x from "./missing";')
    b = analyze_source("src/b.ts", 'export function b() {}')
    graph = build_graph([a, b], ["src/a.ts", "src/b.ts"])
    assert any(e.type == "IMPORTS" and e.target == "file:src/b.ts" for e in graph.edges)
    assert len(graph.unresolved) == 1
