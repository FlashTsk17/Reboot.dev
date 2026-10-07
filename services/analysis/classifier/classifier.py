from pathlib import PurePosixPath
from .models import Classification

EXTENSIONS = {".ts": "TypeScript", ".tsx": "TSX", ".js": "JavaScript", ".jsx": "JSX", ".py": "Python", ".json": "JSON", ".md": "Markdown", ".css": "CSS"}
CONFIG_NAMES = {"package.json", "tsconfig.json", "vite.config.ts", ".env.example", "pyproject.toml"}
IGNORED = {"node_modules", "dist", "build", ".git", ".next", "coverage"}

def classify(path: str, size: int = 0) -> Classification:
    p = PurePosixPath(path); parts = set(p.parts); name = p.name; ext = p.suffix.lower(); reasons: list[str] = []
    if parts & IGNORED:
        category, layer, importance = "GENERATED", "UNKNOWN", "IGNORE"; reasons.append("path is generated or dependency output")
    elif name in CONFIG_NAMES or name.startswith(".") or ext in {".yaml", ".yml", ".toml"}:
        category, layer, importance = "CONFIG", "CONFIG", "MEDIUM"; reasons.append("recognized configuration file")
    elif ext == ".md":
        category, layer, importance = "DOCUMENTATION", "DOCUMENTATION", "LOW"; reasons.append("documentation extension")
    elif "test" in name.lower() or "tests" in parts or "__tests__" in parts:
        category, layer, importance = "TEST", "TEST", "HIGH"; reasons.append("test naming or directory convention")
    elif ext in {".ts", ".tsx", ".js", ".jsx", ".py"}:
        category, layer, importance = "SOURCE", "UNKNOWN", "MEDIUM"
        if "frontend" in parts or ("src" in parts and ("web" in parts or "app" in parts)):
            layer = "FRONTEND"; reasons.append("frontend-oriented path")
        elif "backend" in parts or "api" in parts:
            layer = "BACKEND"; reasons.append("backend/api-oriented path")
        else: reasons.append("recognized source extension")
    elif ext in {".png", ".jpg", ".jpeg", ".svg", ".webp", ".ico"}:
        category, layer, importance = "ASSET", "UNKNOWN", "LOW"; reasons.append("asset extension")
    else:
        category, layer, importance = "UNKNOWN", "UNKNOWN", "LOW"; reasons.append("no deterministic rule matched")
    language = EXTENSIONS.get(ext, "Unknown")
    if size > 1_000_000:
        reasons.append("large file; inspect separately")
        if importance == "MEDIUM": importance = "HIGH"
    return Classification(path, category, language, layer, importance, tuple(reasons))
