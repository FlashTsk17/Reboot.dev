from pathlib import PurePosixPath
from ..ast.models import CodeFileAST
from .models import DependencyGraph, Edge, Node

EXTS = (".ts", ".tsx", ".js", ".jsx")

def resolve_local(source_file: str, specifier: str, files: set[str]) -> str | None:
    if not specifier.startswith("."): return None
    base = PurePosixPath(source_file).parent / specifier
    candidate = str(base)
    for ext in EXTS:
        if candidate + ext in files: return candidate + ext
    for ext in EXTS:
        if candidate + "/index" + ext in files: return candidate + "/index" + ext
    return None

def build_graph(asts: list[CodeFileAST], files: list[str]) -> DependencyGraph:
    graph = DependencyGraph(); file_set = set(files)
    for ast in asts:
        fid = f"file:{ast.path}"; graph.add_node(Node(fid, "FILE", ast.path))
        for symbol in ast.symbols:
            sid = f"symbol:{ast.path}:{symbol.name}"; graph.add_node(Node(sid, symbol.kind.upper(), symbol.name))
            graph.add_edge(Edge(fid, sid, "CONTAINS", ast.path, symbol.line))
        for imp in ast.imports:
            target = resolve_local(ast.path, imp.source, file_set)
            if target:
                tid = f"file:{target}"; graph.add_node(Node(tid, "FILE", target)); graph.add_edge(Edge(fid, tid, "IMPORTS", ast.path, imp.line))
            elif imp.source.startswith("."):
                unresolved = f"unresolved:{ast.path}:{imp.source}"; graph.add_node(Node(unresolved, "UNRESOLVED", imp.source)); graph.unresolved.append(Edge(fid, unresolved, "IMPORTS", ast.path, imp.line))
            else:
                tid = f"package:{imp.source}"; graph.add_node(Node(tid, "PACKAGE", imp.source)); graph.add_edge(Edge(fid, tid, "IMPORTS", ast.path, imp.line))
        for call in ast.calls:
            if call.name in {"fetch", "navigator.share"}: graph.add_edge(Edge(fid, f"external:{call.name}", "CALLS", ast.path, call.line))
    return graph
