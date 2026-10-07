import re
from .models import Call, CodeFileAST, Import, Symbol

IMPORT_RE = re.compile(r"""(?:import\\s+(?:[^;]*?\\s+from\\s+)?|require\\(\\s*)['\"]([^'\"]+)['\"]""")
EXPORT_RE = re.compile(r"""\\bexport\\s+(?:default\\s+)?(?:async\\s+)?(?:function|class|const|let|var)\\s+([A-Za-z_$][\\w$]*)""")
SYMBOL_RE = re.compile(r"""\\b(?:async\\s+)?function\\s+([A-Za-z_$][\\w$]*)\\s*\\(|\\bclass\\s+([A-Za-z_$][\\w$]*)|\\b(?:const|let|var)\\s+([A-Za-z_$][\\w$]*)\\s*=\\s*(?:async\\s*)?(?:\\([^)]*\\)|[A-Za-z_$][\\w$]*)\\s*=>""")
CALL_RE = re.compile(r"""\\b([A-Za-z_$][\\w$]*(?:\\.[A-Za-z_$][\\w$]*)?)\\s*\\(""")

SUPPORTED = {".ts": "TypeScript", ".tsx": "TSX", ".js": "JavaScript", ".jsx": "JSX"}

def analyze_source(path: str, source: str) -> CodeFileAST:
    language = next((v for k,v in SUPPORTED.items() if path.endswith(k)), "Unknown")
    result = CodeFileAST(path=path, language=language)
    lines = source.splitlines()
    for m in IMPORT_RE.finditer(source):
        result.imports.append(Import(m.group(1), source[:m.start()].count("\n")+1))
    for m in EXPORT_RE.finditer(source):
        result.exports.append(m.group(1))
    for i, line in enumerate(lines, 1):
        for m in SYMBOL_RE.finditer(line):
            name = next((x for x in m.groups() if x), None)
            if name:
                kind = "class" if m.group(2) else "function"
                result.symbols.append(Symbol(name, kind, i, i))
        for m in CALL_RE.finditer(line):
            name = m.group(1)
            if name not in {"if", "for", "while", "switch", "catch", "function"}:
                result.calls.append(Call(name, i))
    if "fetch(" in source: result.signals.append("NETWORK_CALL")
    if "navigator.share" in source: result.signals.append("SHARING")
    if re.search(r"password\\s*:", source): result.signals.append("PASSWORD_FIELD")
    return result
